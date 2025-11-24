import serial
import time
import sys

# Verificar que se pasó un argumento
if len(sys.argv) < 2:
    print("Uso: python3 impresora.py <archivo.gcode>")
    sys.exit(1)

filename = sys.argv[1]

# Abrir puerto serial
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=5)
time.sleep(2)

# Homing
ser.write(b"G28\n")
time.sleep(5)  # Esperar a que termine el homing

# Calentar cama y nozzle
ser.write(b"M140 S60\n")  # cama a 60°C
ser.write(b"M104 S200\n") # nozzle a 200°C
ser.write(b"M105\n")      # consulta de temperatura
time.sleep(10)

def print_file(fname):
    with open(fname, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            ser.write((line + "\n").encode())

            while True:
                resp = ser.readline().decode(errors="ignore").strip()
                if resp == "ok":
                    break

print_file(filename)

print(f"Impresion de '{filename}' enviada correctamente.")
