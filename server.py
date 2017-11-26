
# *******************************************************************
# server.py
# Danial Mohammad
# CPSC 471
# Programming Assignment 1
# 11/25/17
# *******************************************************************

import socket
import commands
import sys

#check for parameters
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <PORT_NUMBER>" 
	

# The port on which to listen
serverName = 'ecs.fullerton.edu'

listenPort = int(sys.argv[1])


# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
serverName = ''
welcomeSock.bind((serverName, listenPort))

# Start listening on the socket
welcomeSock.listen(1)

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff
		
# ************************************************
# Receives nothing as parameter
# Receives file from client and writes it locally
# returns nothing
# *************************************************

def getFile():
	newSock, addr = welcomeSock.accept()


	fileNameSize = recvAll(newSock, 10)

	fileName = recvAll(newSock, int(fileNameSize))
	print 'file name : ' + fileName + '\n'

	# The buffer to all data received from the
	# the client.
	fileData = ""

	# The temporary buffer to store the received
	# data.
	recvBuff = ""

	# The size of the incoming file
	fileSize = 0	

	# The buffer containing the file size
	fileSizeBuff = ""

	# Receive the first 10 bytes indicating the
	# size of the file
	fileSizeBuff = recvAll(newSock, 10)

	# Get the file size
	fileSize = int(fileSizeBuff)

	# Get the file data
	fileData = recvAll(newSock, fileSize)

	with open(fileName,'w') as f:
		f.write(fileData)

	newSock.send('SUCCESS')

# ************************************************
# Receives nothing as parameters
# Receives file name from client then beings transfer
# returns nothing
# *************************************************
def sendFile():
	newSock, addr = welcomeSock.accept()

	fileNameSize = recvAll(newSock, 10)
	fileName = recvAll(newSock, int(fileNameSize))
	print 'file name : ' + fileName + '\n'
	
	fileObj = open(fileName, "r")

	# Read 65536 bytes of data
	fileData = fileObj.read(65536)

	# Make sure we did not hit EOF
	if fileData:

		# Get the size of the data read
		# and convert it to string
		dataSizeStr = str(len(fileData))

		# Prepend 0's to the size string
		# until the size is 10 bytes
		while len(dataSizeStr) < 10:
			dataSizeStr = "0" + dataSizeStr

		# Prepend the size of the data to the
		# file data.
		fileData = dataSizeStr + fileData	

		# The number of bytes sent
		numSent = 0		

		# Send the data!
		while len(fileData) > numSent:
			numSent += newSock.send(fileData[numSent:])

	# The file has been read. We are done
	else:
		print 'FAILURE'
		fileObj.close()
		newSock.close()
		exit()		

# ************************************************
# Receives nothing as parameter
# Sends output of ls command to client
# returns nothing
# *************************************************
def printDir():
	newSock, addr = welcomeSock.accept()
	files = commands.getstatusoutput('ls -l')
	numFiles = str(len(files))

	while numFiles < 10:
		numFiles = '0' + numFiles

	newSock.send(numFiles)

	for curr in files:
		newSock.sendall(str(curr))

	newSock.close()

# Wait for connections from client
while True:
	print "Waiting for connections..."
		
	# Accept connections
	clientSock, addr = welcomeSock.accept()

	print "Accepted connection from client: ", addr

	#if client process killed, results in infinite loop - find way to fix
	while True:
		print "Waiting for command..."
		#receive command of length 4 '  ls', ' put', ' get', 'quit'
		cmd = clientSock.recv(4)
		if cmd == ' put':
			print "SUCCESS"
			getFile()		
		elif cmd == ' get':
			print "SUCCESS"
			sendFile()
		elif cmd == '  ls':
			print "SUCCESS"
			printDir()
		elif cmd == 'quit':
			print "SUCCESS"
			clientSock.close()
			break
		else:
			print "FAILURE"
		# Close our side