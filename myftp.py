import sys
import socket
import re
import os

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
    resp = re.split("[()]", resp)

    # hostPort is [h1, h2, h3, h4, p1, p2]
    hostPort = resp[1].split(",")
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
    if (typeCommand("A") == False):
        return False
    
    dataHost, dataPort = pasvCommand()
    if (dataHost == None):
        return False

    controlSocket.send("LIST\r\n")
    
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        dataSocket.connect((dataHost, dataPort))
    except socket.error:
        return False

    resp = controlSocket.recv(1024)

    if (int(resp[0]) != 2 and int(resp[0]) != 1):
        dataSocket.close()
        return False

    data = dataSocket.recv(4096)
    resp = controlSocket.recv(1024)
    print(resp[:-1])
    print(data[:-1])
    dataSocket.close()    
    
def cdCommand(path):
    controlSocket.send("CWD %s\r\n" % path)
    resp = controlSocket.recv(1024)
    if (int(resp[0]) != 2):
        return False
    print(resp[:-1])

def getCommand(pathname):
    if typeCommand("I") == False:
        return False

    dataHost, dataPort = pasvCommand()
    if dataHost == None:
        return False

    controlSocket.send("RETR %s\r\n" % pathname)
    
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        dataSocket.connect((dataHost, dataPort))
    except socket.error:
        return False

    resp = controlSocket.recv(1024)

    if (int(resp[0]) != 2 and int(resp[0]) != 1):
        dataSocket.close()
        return False
    resp = re.split("[()]", resp)[1].split(" ")
    numBytes = int(resp[0])

    data = dataSocket.recv(numBytes)
    resp = controlSocket.recv(1024)

    # Save file in local directory
    fileName = pathname.split("/")[-1]
    localFile = open(fileName, "wb")
    localFile.write(data)
    localFile.close
    dataSocket.close
    print("Succesfully transfered %s (%d bytes) to local machine" % (fileName, numBytes))

def putCommand(pathname):
    # Open file and get file size
    try:
        numBytes = os.path.getsize(pathname)
        localFile = open(pathname, "rb")
    except:
        return False

    if typeCommand("I") == False:
        return False

    dataHost, dataPort = pasvCommand()
    if dataHost == None:
        return False

    controlSocket.send("STOR %s\r\n" % pathname)

    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        dataSocket.connect((dataHost, dataPort))
    except socket.error:
        return False

    resp = controlSocket.recv(1024)

    if (int(resp[0]) != 2 and int(resp[0]) != 1):
        dataSocket.close()
        return False

    dataSocket.send(localFile.read())
    dataSocket.close()

    resp = controlSocket.recv(1024)[:-1]
    if(resp[0] != "2"):
        return False
    
    print(resp)
    print(str(numBytes) + " bytes transfered")

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
        if lsCommand() == False:
            print("ls command failed")
    elif (command[0:2] == "cd"):
        path = command[3:]
        if path == "":
            print("Provide a path name")
            continue
        if cdCommand(path) == False:
            print("cd command failed")
    elif (command[0:3] == "get"):
        pathname = command[4:]
        if pathname == "":
            print("Provide a path name")
            continue
        if getCommand(pathname) == False:
            print("get command failed")
    elif (command[0:3] == "put"):
        pathname = command[4:]
        if pathname == "":
            print("Provide a path name")
            continue

        if putCommand(pathname) == False:
            print("put command failed")
    elif (command[0:6] == "delete"):
        pathname = command[7:]
        if pathname == "":
            print("Provide a path name")
            continue
        controlSocket.send("DELE %s\r\n" % pathname)
        resp = controlSocket.recv(1024)
        print resp[:-1]
    else:
        print("command \"%s\" not recognized" % command.split(" ")[0])

        

        


controlSocket.close()