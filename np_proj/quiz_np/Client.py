from socket import *
import os
import pandas as pd
import numpy as np
np.random.seed(2)
pd.set_option('display.max_columns',1000)
pd.set_option('display.width',1000)





def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


server_ki_ip = "127.0.0.1"
server_defined_port = 33000

client_sock_con = socket(      AF_INET, SOCK_STREAM)

client_sock_con.connect((server_ki_ip, server_defined_port))

msg_ = client_sock_con.recv(1024)  
print (msg_.decode())

while True:

    try:   ans_ = input('Type your msg_ here : ')
    except:pass
    if msg_[1:9] == "Question":
        answer2 = input("do u want to save an ans_? (Y/N):")

        if answer2[0] == 'Y' or answer2[0] == 'y':
            client_sock_con.send(ans_.encode())
        else:
            print ("Ok now give your new ans_ here!\n\n\n\n")
            continue
    elif ans_ == "quit":
        client_sock_con.close()
        exit(0)
    else:
        client_sock_con.send(ans_.encode())
    clear() 
    msg_ = client_sock_con.recv(1024)

    print (msg_.decode())

