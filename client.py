import socket
from cryptography.fernet import Fernet

# Replace with the actual key shared by the server
shared_key = Fernet.generate_key()  # For testing, generate a new key here
cipher = Fernet(shared_key)

# Server configuration
HOST = input("Enter the server IP address (default: 127.0.0.1): ").strip() or "127.0.0.1"
PORT = int(input("Enter the server port (default: 12345): ").strip() or 12345)

def main():
    try:
        print("[*] Connecting to the server...")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print("[*] Connected successfully!")

        print("Type your messages below. Type 'exit' to disconnect.\n")
        while True:
            message = input("> Enter your message: ").strip()
            if message.lower() == "exit":
                print("[-] Disconnecting...")
                break

            encrypted_message = cipher.encrypt(message.encode())
            client.send(encrypted_message)

            reply = client.recv(1024)
            decrypted_reply = cipher.decrypt(reply).decode()
            print(f"Server: {decrypted_reply}")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        client.close()
        print("[*] Connection closed.")

if __name__ == "__main__":
    main()
