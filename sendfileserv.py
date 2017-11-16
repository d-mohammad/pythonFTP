
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import commands
# The port on which to listen
listenPort = 1234

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', listenPort))

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
		
def getFile():
	newSock, addr = welcomeSock.accept()

	fileNameSize = recvAll(newSock, 10)
	fileName = recvAll(newSock, int(fileNameSize))
	print 'file name size: ' + fileNameSize + '\n'
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

	print "The file size is " , fileSize

	# Get the file data
	fileData = recvAll(newSock, fileSize)

	with open(fileName,'w') as f:
		f.write(fileData)


#send to client
def sendFile():
	newSock, addr = welcomeSock.accept()

	fileNameSize = recvAll(newSock, 10)
	fileName = recvAll(newSock, int(fileNameSize))
	print 'file name size: ' + fileNameSize + '\n'
	print 'file name : ' + fileName + '\n'
	
	fileObj = open(fileName, "r")

	# Read 65536 bytes of data
	fileData = fileObj.read(65536)

	# Make sure we did not hit EOF
	if fileData:

		# Get the size of the data read
		# and convert it to string
		dataSizeStr = str(len(fileData))
		print 'data size:' + dataSizeStr

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
		fileObj.close()
		newSock.close()

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
# Accept connections forever
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
		print 'cmd: ' + cmd + '\n'
		if cmd == ' put':
			getFile()
			#putFile needs to have its own connection/teardown
		elif cmd == ' get':
			sendFile()
		elif cmd == '  ls':
			printDir()
		elif cmd == 'quit':
			clientSock.close()
			break
		# Close our side
