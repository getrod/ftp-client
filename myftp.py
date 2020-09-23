import sys
import socket
import re

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
    resp = controlSocket.recv(1024)
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
else:
    print("Username successful")

# Request Password
password = raw_input("Password: ")
controlSocket.send("PASS %s\r\n" % password)
resp = controlSocket.recv(1024)
replyCode = int(resp[0])
if (replyCode != 2):
    print("Password was unsuccessful")
    sys.exit()
else:
    print("Password successful\n")


def pasvCommand():
    '''
    Sends PASV command to ftp server and returns the host and port.
    If PASV fails, the host and port is returned with a value None
    '''
    controlSocket.send("PASV\r\n")
    resp = controlSocket.recv(1024)
    if (int(resp[0]) != 2):
        return None, None
    
    # hostPort is [h1, h2, h3, h4, p1, p2]
    hostPort = re.split("[()]", resp)[1].split(",")
    host = ".".join(hostPort[:4])
    port = int(hostPort[4]) * 256 + int(hostPort[5]) 
    return host, port

def typeCommand(t):
    controlSocket.send("TYPE %s\r\n" % t)
    resp = controlSocket.recv(1024)
    if (int(resp[0]) != 2):
        return False
    return True

def lsCommand():
    controlSocket.send("TYPE A\r\n")
    resp = controlSocket.recv(1024)
    if (int(resp[0]) != 2):
        return False
    return True
    



# FTP program
while True:
    command = raw_input("myftp> ")
    if (command == "quit"):
        print("Quitting ftp session...")
        controlSocket.send("QUIT\r\n")
        resp = controlSocket.recv(1024)
        controlSocket.close()
        break
    elif (command == "ls"):
        
        if (typeCommand("A") == False):
            print("ls command failed")
            continue
        
        dataHost, dataPort = pasvCommand()
        if (dataHost == None):
            print("Pasv failed")
            continue

        controlSocket.send("LIST\r\n")
        
        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            dataSocket.connect((dataHost, dataPort))
        except socket.error:
            print("data socket connection failed")
            continue

        resp = controlSocket.recv(1024)

        if (int(resp[0]) != 2 and int(resp[0]) != 1):
            print("resp failed")
            print(resp)
            dataSocket.close()
            continue

        data = dataSocket.recv(4096)
        print(data)
        dataSocket.close()
        

        


controlSocket.close()