import socket
import threading
from cryptography.fernet import Fernet

# Generate a shared encryption key
shared_key = Fernet.generate_key()
cipher = Fernet(shared_key)

print("[*] Shared encryption key (for testing):", shared_key.decode())

# Server configuration
HOST = input("Enter the IP address to bind the server (default: 0.0.0.0): ").strip() or "0.0.0.0"
PORT = int(input("Enter the port to listen on (default: 12345): ").strip() or 12345)

def handle_client(conn, addr):
    print(f"[+] Connection established with {addr}")
    conn.send(b"Welcome to the secure chat server! Type 'exit' to disconnect.")

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            decrypted_message = cipher.decrypt(data).decode()
            print(f"[{addr}] {decrypted_message}")

            if decrypted_message.lower() == "exit":
                print(f"[-] {addr} disconnected.")
                break

            encrypted_reply = cipher.encrypt(f"Received: {decrypted_message}".encode())
            conn.send(encrypted_reply)
        except Exception as e:
            print(f"[!] Error handling {addr}: {e}")
            break

    conn.close()

# Start the server
def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[*] Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
    except Exception as e:
        print(f"[!] Server error: {e}")
    finally:
        print("[*] Shutting down the server...")

if __name__ == "__main__":
    main()
