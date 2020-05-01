import os
import shutil
from Crypto.Hash import HMAC, SHA256


'''
Putting this here for future use. Essentially this is the server side logic for
generating the derived keys from the nonces sent by the client. This should be
in the pipeline for the whole message send / receive / decrypt flow. These keys
will be used to decrypt the in app commands sent from the client. This is assuming
that msg in this case is of type bytes where it has the following format:

label | nonce

where label is either b'msg' or b'mac' what the following nonce will be used to
create.

label, nonce = msg[:-256], msg[-256:]

if (label == b'msg'):
    msg_key = self.generate_derived_key(session_msg_key, nonce)
    print("msg_key:", msg_key.hex())

if (label == b'mac'):
    mac_key = self.generate_derived_key(session_mac_key, nonce)
    print("mac_key:", mac_key.hex())
'''

#server is address A
class Server:
    def __init__(self):
        self.current_client = "B"
        self.current_client_dir = "./NETWORK/A/DATA/" + self.current_client + "/"

    def upload_file(self, file):
        if not os.path.exists(self.current_client_dir + file):
            pass


    def download_file(self, filename):
        path = self.current_client_dir + filename
        if not os.path.exists(path):
            print ("This file does not exist")
        else:
            f = open(path, "r")
            msg_str = f.read()
            msg_bytes = msg_str.encode('ascii')



    def parse_command(self, plaincomm):
        args = plaincomm.split()
        cmd = (args[0]).upper()
        if cmd == "MKD":    #make directory
            new_dir = self.current_client_dir + args[1]
            os.mkdir(new_dir)
        elif cmd == "RMD":  #remove directory
            dir_arg = args[1]
            if not os.path.exists(self.current_client_dir + dir_arg):
                print ("This folder does not exist!")
            else:
                shutil.rmtree(self.current_client_dir + dir_arg, ignore_errors=True)
        elif cmd == "GWD":  #get working directory
            msg_bytes = self.current_client_dir.encode('ascii')
            #send message! TODO
        elif cmd == "CWD":  #change directory
            dir_arg = args[1]
            path = self.current_client_dir + dir_arg
            print (path)
            if not os.path.exists(path) or (not (self.current_client + "..") in path):
                #tries to make sure user can't back out of their own folder into other folders - kinda hacky
                print ("This folder does not exist!")
            else:
                self.current_client_dir = self.current_client_dir + dir_arg
        elif cmd == "LST": #list contents
            lst = os.listdir(self.current_client_dir)
            msgstr = "\t".join(lst)
            msg_bytes = msgstr.encode('ascii')
            #SEND MESSAGE TODO
        elif cmd == "UPL":
            self.upload_file(args[1])   #TODO?? i am confused on how to do this
        elif cmd == "DNL":  #download file
            self.download_file(args[1])
        elif cmd == "RMF":  #rm file from folder
            print (self.current_client_dir + args[2] + + "/" + args[1])
            os.remove(self.current_client_dir + args[2] + + "/" + args[1])   #check formatting
        else:
            msg_str = "Command not found"
            msg_bytes = msg_str.encode('ascii')

    '''
    Uses the nonce sent over from the client to generate the derived message or
    mac keys.

    ARGUMENTS:
    key - bytes: either the session message key or the session mac key
    nonce - bytes: the nonce used to generate the derived keys

    RETURNS:
    bytes: the appropriate derived key
    '''
    def generate_derived_key(self, key, nonce):
        return HMAC.new(key, msg=nonce, digestmod=SHA256).digest()
