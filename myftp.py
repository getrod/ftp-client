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

'''
def pasvCommand():
    controlSocket.send("PASV\r\n")
    resp = controlSocket.recv(1024)
'''  

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
        '''
        controlSocket.send("TYPE A\r\n")
        resp = controlSocket.recv(1024)
        if (int(resp[0]) != 2):
            print("ls command failed")
            continue
        else:
            print("type a completed successfully")
        '''
        if(lsCommand()):
            print("type a passed")
        else:
            print("type a failed")

        


controlSocket.close()