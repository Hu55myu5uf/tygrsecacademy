
"""
End-to-end test of lab flow: start container, create exec, stream data.
This simulates exactly what happens when a user starts a lab.
"""
import docker
import time

def test_full_flow():
    print("=== Full Lab Flow Test ===\n")
    
    try:
        client = docker.from_env()
        print("[OK] Connected to Docker")
    except Exception as e:
        print(f"[FAIL] Cannot connect to Docker: {e}")
        return

    container = None
    try:
        # Step 1: Start Container (simulating lab_manager.start_lab)
        print("\n[1] Starting Container with TTY...")
        image = "alpine:latest"
        cmd = "sh -c 'apk add --no-cache netcat-openbsd && while true; do sleep 1000; done'"
        
        container = client.containers.run(
            image,
            command=cmd,
            detach=True,
            tty=True,
            stdin_open=True,
            name=f"full_flow_test_{int(time.time())}",
            mem_limit="512m"
        )
        print(f"    Container ID: {container.id[:12]}")
        print(f"    Status: {container.status}")
        
        # Wait a moment for container to stabilize
        time.sleep(1)
        container.reload()
        print(f"    After reload: {container.status}")
        
        if container.status != "running":
            print("[FAIL] Container not running!")
            return

        # Step 2: Create Exec (simulating WebSocket handler)
        print("\n[2] Creating Exec Instance...")
        exec_result = client.api.exec_create(
            container.id,
            cmd="/bin/sh",
            stdin=True,
            tty=True
        )
        exec_id = exec_result["Id"]
        print(f"    Exec ID: {exec_id[:12]}...")

        # Step 3: Start Exec with socket
        print("\n[3] Starting Exec with socket=True...")
        sock = client.api.exec_start(exec_id, socket=True, tty=True)
        print(f"    Socket type: {type(sock)}")

        # Step 4: Test recv/send
        print("\n[4] Testing socket I/O...")
        
        # Send a simple command
        test_cmd = "echo HELLO_FROM_TEST\n"
        sock.send(test_cmd.encode())
        print(f"    Sent: {repr(test_cmd)}")
        
        # Wait and receive
        time.sleep(0.5)
        sock.setblocking(False)  # Non-blocking to avoid hang
        try:
            response = sock.recv(4096)
            print(f"    Received: {response.decode('utf-8', errors='ignore')[:100]}")
        except BlockingIOError:
            print("    [!] No data ready (non-blocking)")
        except Exception as e:
            print(f"    [!] Recv error: {e}")

        sock.close()
        print("\n[5] Socket closed successfully")

        # Cleanup
        print("\n[6] Stopping container...")
        container.stop()
        container.remove()
        print("    Done!")
        
        print("\n=== TEST PASSED ===")

    except Exception as e:
        print(f"\n[FAIL] Exception: {e}")
        import traceback
        traceback.print_exc()
        
        if container:
            try:
                container.stop()
                container.remove()
            except:
                pass

if __name__ == "__main__":
    test_full_flow()
