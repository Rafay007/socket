from socket import *
import threading
import time
import pandas as pd
import numpy as np
np.random.seed(2)
pd.set_option('display.max_columns',1000)
pd.set_option('display.width',1000)

global i
i = 0

class Quiz_server():
    def new_client_con(self, client, addr):
        global i
        chk=False
        while True:
            client.send("Quiz app started \n".encode()) 
            authentication = client.recv(1024) 
            print(authentication)

            client.send("enter your name ".encode())
            m1 = client.recv(1024) 
            m1=m1.decode("utf-8")
            name, surname = m1.split() 

            client.send("enter your pass".encode())
            password = client.recv(1024) 
            password=password.decode("utf-8")
            print( "name: ", name)
            print ("pass: ", password)

            file = open(r"D:\np_proj\quiz_np\students.txt", "r") #Open students txt file
            str_file = file.read() 
            arr=str_file.split('\n')
            for cred in arr:
                more=cred.split(' ')
                if str(more[0])==str(name):
                    if str(more[1])==str(surname):
                        if str(more[2])==str(password):
                            chk=True
                            break

            if chk: 
                if chk: 
                    
                    client.send("authenticated \n".encode()) 
                    file2 = open(r"D:\np_proj\quiz_np\attendance.txt", "w")	#open the authentication txt file
                    file2.write(name) 
                    file2.write(": yes") 
                    file2.close() 

                    loc_for_time_1 = time.localtime(time.time())[4]
                    print( "Time  : ", time.localtime(time.time())[3], ":", time.localtime(time.time())[4])

                    questionFile = open(r"D:\np_proj\quiz_np\questions.txt", "r")
                    questions = questionFile.read()
                    questions = [y for y in (x.strip() for x in questions.splitlines()) if y]
                    questionFile.close()

                    answerFile = open(r"D:\np_proj\quiz_np\answers.txt","r")
                    answers = answerFile.read()
                    answers = [y for y in (x.strip() for x in answers.splitlines()) if y]
                    answerFile.close()
                    points = 0
                    for number in range(0, len(questions)): 
	                    client.send(questions[number].encode())
	                    answer = client.recv(1024).decode()
	                    if str(answer.lower()) == str(answers[number]):
	                    	points = points + 10
                    
                    loc_for_time_2 = time.localtime(time.time())[4]
                    time_dur = loc_for_time_2 - loc_for_time_1
                    if time_dur > 30:
                        print ("time is up bro\n")
                        client.close()
                    print (name, surname, "--points--", str(points), "--bonus--",  str(10/(time_dur+1)), "--total Score--:",str(points + 10/(time_dur+1)))
            else:
                client.send("Authentication cannot be completed bharr may jao.\n".encode())

            i = i + 1
            file.close()


    def __init__(self, serverPort, serverName):
        try:
            serverSocket = socket(AF_INET, SOCK_STREAM)
        except:
            print ("socket cannot be initiated")
            exit(1)
        print ("Socket is initiated")
        try:
            serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except:
            print ("Socket cannot used now")
            exit(1)
        print ("Socket is used")
        try:
            serverSocket.bind((serverName, serverPort))
        except:
            print ("Binding cannot perform")
            exit(1)
        print( "Binding is done!")
        try:
            serverSocket.listen(45)
        except:
            print ("sorry server cannot connect now for some reason")
            exit(1)
        print ("server is running and listening")

        while True:
            connectionSocket, addr = serverSocket.accept()

            threading.Thread(target=self.new_client_con, args=(connectionSocket, addr)).start()

if __name__ == "__main__":
    serverName = "127.0.0.1"
    serverPort = 33000
    Quiz_server(serverPort, serverName)

