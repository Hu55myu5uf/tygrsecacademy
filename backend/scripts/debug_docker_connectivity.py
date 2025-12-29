
import docker
import time

def debug_docker():
    print("Testing Docker Socket Methods...")
    try:
        client = docker.from_env()
    except Exception as e:
        print(f"FAILED to connect to Docker: {e}")
        return

    try:
        print("Starting Test Container...")
        container = client.containers.run(
            "alpine:latest",
            command="tail -f /dev/null", 
            detach=True,
            tty=True,
            stdin_open=True,
            name=f"test_socket_methods_{int(time.time())}"
        )
        print(f"Container ID: {container.id[:12]}")

        print("\nCreating Exec...")
        exec_id = client.api.exec_create(
            container.id,
            cmd="/bin/sh",
            stdin=True,
            tty=True
        )["Id"]

        print("Starting Exec (socket=True)...")
        sock = client.api.exec_start(exec_id, socket=True, tty=True)
        
        print(f"\nSocket Type: {type(sock)}")
        print(f"\nAvailable Methods on Socket:")
        methods = [m for m in dir(sock) if not m.startswith('_')]
        for m in methods:
            print(f"  - {m}")

        # Test common methods
        print("\n--- Testing Methods ---")
        for method_name in ['recv', 'read', 'send', 'write', 'sendall', 'fileno']:
            has_method = hasattr(sock, method_name)
            print(f"  {method_name}: {'YES' if has_method else 'NO'}")

        print("\nStopping Container...")
        container.stop()
        container.remove()
        print("Done.")

    except Exception as e:
        print(f"\n[!] FAILURE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_docker()
