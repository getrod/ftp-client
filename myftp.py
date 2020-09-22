import sys
import socket

# Ensure user gives at least one argument
if (len(sys.argv) - 1 < 1):
    print("Missing ftp server host name")
    sys.exit()

# Try to connect to ftp server
controlServerName = sys.argv[1]
controlServerPort = 21
controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    print("Connecting to " + controlServerName + "...")
    controlSocket.connect((controlServerName, controlServerPort))
except socket.error:
    print("Could not connect to " + controlServerName)
    sys.exit()

print("Connection Successful")
controlSocket.close()