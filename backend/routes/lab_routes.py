
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from sqlalchemy.orm import Session
from typing import List
import json
import asyncio

from database.connection import get_db
from models.user import User
from models.labs import Lab, LabInstance, LabInstanceStatus
from services.lab_manager import lab_manager
from auth.rbac import get_current_user

router = APIRouter()

# Dependency to get current user/admin
# Dependency to get current user/admin
# Note: WebSockets have different auth handling

# Dependency to get current user/admin
# Note: WebSockets have different auth handling

@router.get("/", response_model=List[dict])
async def get_all_labs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all available labs"""
    labs = db.query(Lab).filter(Lab.is_active == True).all()
    return [
        {
            "id": l.id,
            "title": l.title,
            "description": l.description,
            "difficulty": l.difficulty,
            "category": l.category,
            "estimated_minutes": l.estimated_minutes
        }
        for l in labs
    ]

@router.get("/{lab_id}", response_model=dict)
async def get_lab_details(
    lab_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get full details for a lab"""
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
        
    return {
        "id": lab.id,
        "title": lab.title,
        "description": lab.description,
        "content": lab.content,  # Contains markdown instructions
        "difficulty": lab.difficulty,
        "category": lab.category,
        "time_limit": 60, # Default or from DB
        "objectives": [] # Can be expanded with real objectives table
    }

@router.post("/{lab_id}/start", response_model=dict)
async def start_lab(
    lab_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start a lab instance"""
    # 1. Verify Lab exists
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")

    # 2. Start Instance via Manager
    try:
        instance = lab_manager.start_lab(db, current_user.id, lab_id)
        return {
            "instance_id": instance.id,
            "status": instance.status,
            "container_id": instance.container_id,
            "message": "Lab started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/instances/{instance_id}/stop")
async def stop_lab(
    instance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Stop a running lab instance"""
    instance = db.query(LabInstance).filter(
        LabInstance.id == instance_id,
        LabInstance.user_id == current_user.id
    ).first()
    
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
        
    lab_manager.stop_lab(db, instance_id)
    return {"message": "Lab stopped"}

@router.websocket("/ws/{instance_id}")
async def lab_terminal_websocket(websocket: WebSocket, instance_id: int, db: Session = Depends(get_db)):
    """
    WebSocket endpoint for terminal streaming.
    """
    print(f"[WS DEBUG] Connection attempt for instance_id={instance_id}")
    await websocket.accept()
    print(f"[WS DEBUG] WebSocket accepted")
    
    # 1. Get Instance & Container ID
    instance = db.query(LabInstance).filter(LabInstance.id == instance_id).first()
    print(f"[WS DEBUG] Instance query result: {instance}")
    
    if not instance:
        print(f"[WS DEBUG] Instance not found!")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    print(f"[WS DEBUG] Instance status={instance.status}, container_id={instance.container_id}")
    
    if not instance.container_id or instance.status != LabInstanceStatus.RUNNING:
        print(f"[WS DEBUG] Instance not running or no container_id!")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    container_id = instance.container_id
    print(f"[WS DEBUG] Proceeding with container_id={container_id[:12]}...")
    
    # 2. Create Exec Instance (pseudo-terminal)
    try:
        if not lab_manager.client:
            print(f"[WS DEBUG] Docker client is None!")
            await websocket.send_text("Docker service unavailable")
            await websocket.close()
            return

        print(f"[WS DEBUG] Creating exec...")
        exec_id = lab_manager.client.api.exec_create(
            container_id,
            cmd="/bin/sh",
            stdin=True,
            tty=True
        )["Id"]
        print(f"[WS DEBUG] Exec created: {exec_id[:12]}...")
        
        # 3. Start Exec and get socket
        print(f"[WS DEBUG] Starting exec with socket=True...")
        sock = lab_manager.client.api.exec_start(exec_id, socket=True, tty=True)
        print(f"[WS DEBUG] Socket obtained: {type(sock)}")
        
    except Exception as e:
        import traceback
        print(f"[WS DEBUG] Exec setup FAILED: {e}")
        traceback.print_exc()
        await websocket.close()
        return

    # 4. Pipe Data
    # Python's docker-py socket is a raw socket. We need to bridge it with FastAPI's WebSocket.
    # This loop runs in a separate task
    
    # NOTE: This implementation is complex because docker raw socket is blocking/low-level.
    # A robust production solution uses a specific proxy or library (like aio-docker).
    # For this MVP, we will try a simple read/write loop if possible, 
    # but mixing sync socket with async websocket is prone to blocking the event loop.
    # We'll use a ThreadPoolExecutor for the blocking socket read.

    loop = asyncio.get_event_loop()

    async def forward_from_docker():
        """Read from docker socket and send to websocket"""
        try:
            while True:
                # sock.recv is blocking, run in thread
                data = await loop.run_in_executor(None, sock.recv, 4096)
                if not data:
                    break
                await websocket.send_text(data.decode('utf-8', errors='ignore'))
        except Exception as e:
            print(f"Error reading from docker: {e}")
        finally:
            await websocket.close()

    async def forward_to_docker():
        """Read from websocket and write to docker socket"""
        try:
            while True:
                data = await websocket.receive_text()
                # Write to docker socket
                sock.send(data.encode())
        except WebSocketDisconnect:
            pass
        except Exception as e:
            print(f"Error writing to docker: {e}")

    # Run tasks
    try:
        # Create tasks
        task_read = asyncio.create_task(forward_from_docker())
        task_write = asyncio.create_task(forward_to_docker())
        
        # Wait for either to finish (usually WS disconnect)
        done, pending = await asyncio.wait(
            [task_read, task_write],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        for task in pending:
            task.cancel()
            
    except Exception as e:
        print(f"WS Loop Error: {e}")
    finally:
        sock.close()
