import socket
import os
import json
from _thread import *
import zlib
import re



serverSocket = socket.socket()


clients = []
user_count = 0
 


host = ''
port = 1048

print('Waiting for connection')

try:
    serverSocket.bind((host, port))
except socket.error as e:
    print(str(e))

serverSocket.listen(10)
serverSocket.settimeout(30)


def client_thread(current_client):
	while True:
		msg = current_client.recv(1048)
		packetNum, correctsum, msg, flag = split_message(msg,0)
		flag = flag.split(' ')[1]
		if(flag == "\"ESTAB\""):
			name = msg
			add_client(current_client, name)
			name = name.split("\"")[1]
			print(name + " has connected")
			message = "you have been conected"
			send_message(0,message,"REPLY",current_client,0)
		elif(flag == quit):
			break
		
		msg = current_client.recv(1048)
		packetNum, correctsum, msg, flag = split_message(msg,0)
		flag = flag.split(' ')[1]
		
		if(flag == "\"BROADCAST\""):
			symptom = symptomTestResult(msg)
			send_message(10,symptom,"REPLY",current_client,0)
			if(len(clients)>=0):
				message ="multi"
				send_message(4,message,"REPLY",current_client,0)
				data = current_client.recv(1048)
				packetNum, correctsum, msg, flag = split_message(data,0)
				msg = msg[1:len(msg)]
				if(msg == "\"yes\""):
					sendToAll(symptom,name)
			else:
				message ="not multi"
				send_message(4,message,"REPLY",current_client,0)
		elif(flag == quit):
			break
	connection.close()


def add_client(current_client,msg):
	temp = [current_client,msg]
	clients.append(temp)



def sendToAll(symptom, name):
	for i in range(0,len(clients)):
		if(clients[i][1] != name):
			message = name + " has " + symptom + " symptoms"
			send_message(1,message,"BROADCAST",clients[i][0],0)




def send_message(packetNum,message,flagType,client,count):
	package = {
		"packetNum": packetNum,
		"checksum": checksum(message),
		"message": message,
		"flagType": flagType,
	}
	data = json.dumps(package)
	client.send(data.encode("ascii"))
	if count < 10:
		temp = client.recv(1048)
		count = count + 1
		print(count)
		packetNum_check, correctsum_check, msg_check, flag_check = split_message(temp,9)
		if(msg_check[1:len(msg_check)] == "\"resend\""):
			send_message(packetNum,message,flagType,client,count)
	return count


	


def symptomTestResult(msg):
	mild_symptoms = ["cough","sneeze"]
	severe_symptoms = ["loss of smell","loss of taste"]
	msg = msg[2:len(msg)-1]
	temp = msg.split(", ")

	mild = 0
	severe = 0

	for i in range(0,len(temp)):
		if temp[i].lower() in mild_symptoms:
			mild += 1
		if temp[i].lower() in severe_symptoms:
			severe += 1

	if severe > 0:
		symptom = "severe"	
	elif severe == 0 and mild >= 2: 
		symptom = "mild"
	else:
		symptom = "none"

	return symptom


def split_message(msg,count):
	print("split")
	msg.decode() 
	package = re.split("{|:|,|}", msg)
	if count <10:

		if checksum_check(package[8], package[4]) and count < 10:
			print("checksum failed")
			print(count)
			message ="resend"
			send_message(0,message,"NCK",current_client,0)
			print("secound")
			msg = current_client.recv(1048)
			count = count + 1
			count = split_message(msg,count)

		print(package[8][1:len(package[8])] != "\"recived\"")
		if(package[4][1:len(package[4])] != "\"recived\""):
			print("checksum passed")
			message = "recived"
			count = send_message(0,message,"ACK",current_client,100)
			print("this message has been sent")
		
	print("end of split")
	return package[2], package[8], package[4], package[6]




def checksum_check(correct_checksum, data):
	return int(correct_checksum[1:len(correct_checksum)]) != checksum(data[2:len(data)-1])

		

def checksum(data):
 checksum = zlib.adler32(data)
 return checksum



while user_count < 4:


	current_client, address = serverSocket.accept()
	start_new_thread(client_thread, (current_client, ))
	user_count += 1 
if  user_count == 4:
	current_client, address = serverSocket.accept()
	message = ("DNS")
	send_message(0,message,"NCK",current_client,0)
	print("too many users")
	


serverSocket.close()




	











		

	
		
					

