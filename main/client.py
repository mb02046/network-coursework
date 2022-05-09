import socket
import json
import sys
import re
import time


def send_message(packetNum,message,flagType,count):
	package = {
		"packetNum":packetNum,
		"checksum":checksum(message),
		"message":message,
		"flagType":flagType,
	}
	data = json.dumps(package)
	ClientSocket.send(data.encode("ascii"))


	if count < 10:
		temp = ClientSocket.recv(1048)
		count = count + 1
		packetNum_check, correctsum_check, msg_check, flag_check = split_message(temp,10)
		if(msg_check[1:len(msg_check)] == "\"resend\""):
			send_message(packetNum,message,flagType,count)		
	
	return count

def split_message(msg,count):
	msg.decode()
	package = re.split("{|:|,|}", msg)
	if count < 10:
		if checksum_check(package[8], package[4]) and count < 10:
			print("checksum failed")
			message ="resend"
			send_message(0,message,"NCK",count)
			msg = ClientSocket.recv(1048)
			count = count + 1
			count = split_message(msg,count)
		
		if(package[4][1:len(package[4])] != "\"recived\""):
			message ="recived"
			count = 100
			count =send_message(0,message,"ACK",100)
			
	return package[2], package[8], package[4], package[6]


def checksum_check(correct_checksum, data):
	return int(correct_checksum[1:len(correct_checksum)]) != checksum(data[2:len(data)-1])
		
import zlib
def checksum(data):
 checksum = zlib.adler32(data)
 return checksum

ClientSocket = socket.socket()
host = ''
port = 1048

print('Waiting for connection')

try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

message = raw_input("What are your names: ")
send_message(0,message,"ESTAB",0)
while True:
	option = input("select option \n 1. enter sysptoms \n  2. quit \n (1/2): ") 
	temp = ClientSocket.recv(1048)
	packetNum, correctsum, msg, flag = split_message(temp,0)
	msg = msg[2:len(msg)]
	if(msg == "DNS")
		print("too many users")
		break
	if option == 1:	
		message = raw_input('What are you sysptoms: ')
		send_message(1,message,"BROADCAST",0)
		temp = ClientSocket.recv(1048)
		packetNum, correctsum, msg, flag = split_message(temp,0)
		msg = msg[2:len(msg)-2]
		print("you have "+ msg + " symptoms")

		temp = ClientSocket.recv(1048)
		packetNum, correctsum, msg, flag = split_message(temp,9)

		flag = flag[1:len(flag)]
		msg = msg[2:len(msg)]
		if(flag == "\"REPLY\"" and msg == "multi"):
			mag = raw_input("do you want to send your syspomts to everyone, yes or no")
			send_message(packetNum,mag,"BROADCAST",0)
	elif option == 2:
		message = "quit"
		send_message(2,message,QUIT)
		break

	#while True:	
	#	temp = ClientSocket.recv(1048)
	#	packetNum, correctsum, msg, flag = split_message(temp,0) 
	
	


ClientSocket.close()


