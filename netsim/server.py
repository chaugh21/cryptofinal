import os
import shutil
from Crypto.Hash import HMAC, SHA256


'''
Putting this here for future use. Essentially this is the server side logic for
generating the derived keys from the nonces sent by the client. This should be
in the pipeline for the whole message send / reciept / decrypt flow. These keys
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
        self.current_client_dir = "./NETWORK/" + current_client + "/DATA"
        self.pwds = {}

    def upload_file(self, filepath):
        #where are the server files stored??
        shutil.copy(filepath, "./NETWORK/S/" + self.current_client_dir, True)

    def download_file(self, filename):
        if not os.path.exists("./NETWORK/S" + self.current_client_dir):
            return ("This file does not exist")
        shutil.copy("./NETWORKS/S" + self.current_client_dir + "/" + filename, self.current_client_dir, True) #is it right to be copying to network/client/in?

    def parse_command(self, plaincomm):
        args = plaincomm.split()
        cmd = (args[0]).upper()
        if cmd == "MKD":
            new_dir = self.client_dir + args[1]
            os.mkdir(new_dir)
            return  #do we want to give result?
        elif cmd == "RMD":
            dir_arg = args[1]
            if not os.path.exists(self.client_dir + dir_arg):
                print ("This folder does not exist!")
            else:
                shutil.rmtree(self.client_dir + dir_arg, ignore_errors=True)
            return
        elif cmd == "GWD":
            return os.getcwd() #check
        elif cmd == "CWD":
            os.chdir(self.client_dir + args[1])  #check if this is allowed and if it exists
            return
        elif cmd == "LST":
            return os.listdir() #type list
        elif cmd == "UPL":
            self.upload_file(args[1])
            return
        elif cmd == "DNL":
            self.download_file(args[1], dst)
            return
        elif cmd == "RMF":
            os.remove(PATH + args[2] + "/" + args[1])   #check formatting
            return
        else:
            return "Command not found"

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
