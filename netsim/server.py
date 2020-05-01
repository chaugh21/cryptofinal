import os
import shutil
from Crypto.Hash import HMAC, SHA256
import encrypt


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
    def __init__(self, curr_client):
        self.current_client = curr_client
        self.current_client_dir = "./NETWORK/A/DATA/" + self.current_client + "/"

    def download_file(self, netif, filename):
        path = self.current_client_dir + filename
        if not os.path.exists(path):
            msg_str = "This file does not exist!"
            msg_bytes = msg_str.encode('ascii')
            self.encrypt_and_send(netif, msg_bytes)
        else:
            f = open(path, "r")
            msg_str = f.read()
            msg_bytes = msg_str.encode('ascii')
            f.close()
            self.encrypt_and_send(netif, msg_bytes)

    def get_msg_mac_keys(self):
        #more stuff here
        return msg_key, mac_key
    
    def get_sqn_number(self):
        #stuff here
        return sqn_number

    '''used in parse_command, encrypts and sends a message to the client'''
    def encrypt_and_send(self, netif, msg_bytes):       
            msg_key, mac_key = self.get_msg_mac_keys()
            sqn_number = self.get_sqn_number()
            encrypt_instance = encrypt(msg_bytes, msg_key, mac_key, sqn_number)
            netif.send_msg(self.current_client, msg_bytes.encode('utf-8'))
            return

    '''This function takes in a decrypted command and executes it, encrypting and sending back a message to the client if necessary'''
    def parse_command(self, plaincomm):     #COMMAND NEEDS TO BE DECRYPTED BEFORE THIS IS CALLED
        #test
        netif = network_interface("./NETWORK/","A")    #initialize network
        args = plaincomm.split()
        cmd = (args[0]).upper()
        if cmd == "MKD":    #make directory
            new_dir = self.current_client_dir + args[1]
            os.mkdir(new_dir)
        elif cmd == "RMD":  #remove directory
            dir_arg = args[1]
            if not os.path.exists(self.current_client_dir + dir_arg):   #if this is invalid path
                msg_str = "This folder does not exist!"
                msg_bytes = msg_str.encode('ascii')
                self.encrypt_and_send(netif, msg_bytes)
            else:
                shutil.rmtree(self.current_client_dir + dir_arg, ignore_errors=True)
        elif cmd == "GWD":  #get working directory
            msg_bytes = self.current_client_dir.encode('ascii')
            self.encrypt_and_send(netif, msg_bytes)
        elif cmd == "CWD":  #change directory
            dir_arg = args[1]
            path = self.current_client_dir + dir_arg
            print (path)
            if not os.path.exists(path):    #doesnt actually ensure this is allowed...
                msg_str = "This folder does not exist!"
                msg_bytes = msg_str.encode('ascii')
                self.encrypt_and_send(netif, msg_bytes)
            else:
                self.current_client_dir = self.current_client_dir + dir_arg
        elif cmd == "LST": #list contents
            lst = os.listdir(self.current_client_dir)
            msgstr = "\t".join(lst)
            msg_bytes = msgstr.encode('ascii')
            self.encrypt_and_send(netif, msg_bytes)
        elif cmd == "UPL":  #form of upl FILENAME FILECONTENT
            filename = args[1]
            dafile = " ".join(args[2:])
            f = open(self.current_client_dir + filename, "w+")
            f.write(dafile)
            f.close()
        elif cmd == "DNL":  #download file
            self.download_file(netif, args[1])
        elif cmd == "RMF":  #rm file from folder        #in form of "rmf FILE FOLDER"
            #print (self.current_client_dir + args[2] + "/" + args[1])
            os.remove(self.current_client_dir + args[2] + "/" + args[1])   #check formatting
        else:
            msg_str = "Command not found"
            msg_bytes = msg_str.encode('ascii')
            self.encrypt_and_send(netif, msg_bytes)

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
