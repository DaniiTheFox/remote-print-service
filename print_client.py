import socket
import os
import sys

if len(sys.argv) < 3:
    print("Uso: python3 cliente.py <ip_servidor> <archivo.gcode>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
FILEPATH = sys.argv[2]

filename = os.path.basename(FILEPATH)
size = os.path.getsize(FILEPATH)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, 5000))

    # 1. Enviar nombre
    s.send(filename.encode())
    s.recv(1024)

    # 2. Enviar tamaño
    s.send(str(size).encode())
    s.recv(1024)

    # 3. Enviar datos
    with open(FILEPATH, "rb") as f:
        s.sendall(f.read())

print(f"Archivo '{filename}' enviado correctamente.")
