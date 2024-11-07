import socket
import threading
import time
import platform
import subprocess

SERVER_HOST = "0.0.0.0"       
SERVER_PORT = 8080            
CLIENT_PORT = 8082            
TARGET_IP = "192.168.1.102"   

def clear():
    osnames = platform.system()
    subprocess.run(['cls' if osnames == "Windows" else 'clear'], shell=True)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

def receive_messages():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[Connected] with {client_address}")
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[Received] {message}")
        client_socket.close()

def send_messages():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False

    while not connected:
        try:
            client_socket.connect((TARGET_IP, CLIENT_PORT))
            connected = True
            print(f"[Connected] to {TARGET_IP}:{CLIENT_PORT} to send messages.")
        except ConnectionRefusedError:
            print("[!] Connection failed. Retrying in 3 seconds...")
            time.sleep(3)

    while True:
        message = input("Enter message: ")
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))
    client_socket.close()

receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()
