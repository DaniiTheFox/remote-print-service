import socket
import subprocess
import os

HOST = "0.0.0.0"
PORT = 5000

def recibir_archivo(conn):
    filename = conn.recv(1024).decode().strip()
    conn.send(b"FILENAME_OK")

    size = int(conn.recv(1024).decode().strip())
    conn.send(b"SIZE_OK")

    data = b""
    while len(data) < size:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk

    with open(filename, "wb") as f:
        f.write(data)

    print(f"Archivo recibido: {filename} ({size} bytes)")
    return filename


def iniciar_impresion(filename):
    print(f"Iniciando impresión de: {filename}")
    subprocess.run(["python3", "print.py", filename])


def main():
    print(f"Servidor escuchando en puerto {PORT}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            print(f"Cliente conectado: {addr}")

            with conn:
                filename = recibir_archivo(conn)
                iniciar_impresion(filename)


if __name__ == "__main__":
    main()
