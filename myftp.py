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
    print(controlSocket.recv(1024))
except socket.error:
    print("Could not connect to " + controlServerName)
    sys.exit()

print("Connection Successful")

# Request username
username = raw_input("Username: ")
controlSocket.send("USER %s\r\n" % username)
resp = controlSocket.recv(1024)
replyCode = int(resp[0])
if (replyCode != 2 and replyCode != 3):
    print("Username was unsuccessful")
    sys.exit()

# Request Password
password = raw_input("Password: ")
controlSocket.send("PASS %s\r\n" % password)
resp = controlSocket.recv(1024)
replyCode = int(resp[0])
if (replyCode != 2):
    print("Password was unsuccessful")
    sys.exit()

controlSocket.close()