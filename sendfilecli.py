
# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys

# Command line checks 
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <PORT_NUMBER>" 

# Server address
serverAddr = "localhost"

# Server port
serverPort = int(sys.argv[1])

# The name of the file

# Open the file

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

# The number of bytes sent
numSent = 0

# The file data
fileData = None

def sendFile(connSock, splitInput):
	fileName = splitInput[1]
	fileObj = open(fileName, "r")

	# Read 65536 bytes of data
	fileData = fileObj.read(65536)

	# Make sure we did not hit EOF
	if fileData:
		fileNameSize = str(len(fileName))
		#fixed length header indicating file name size
		while len(fileNameSize) < 10:
			fileNameSize = "0" + fileNameSize
		
		connSock.send(fileNameSize + fileName)

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
			numSent += connSock.send(fileData[numSent:])

	# The file has been read. We are done
	else:
		fileObj.close()


# Keep sending until all is sent
while True:
	userInput = raw_input("\nWaiting for command...\n")
	splitInput = userInput.split()
	cmd = splitInput[0]
	connSock.send(cmd)

	if cmd == 'put':
		sendFile(connSock, splitInput)
	elif cmd == 'quit':
		break

print "Sent ", numSent, " bytes."
	
# Close the socket and the file
connSock.close()

	


