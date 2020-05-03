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
    def __init__(self, curr_client, netif, encrypt_instance):
        self.current_client = curr_client
        self.netif = netif
        self.current_client_dir = "./NETWORK/A/DATA/" + self.current_client + "/"
        self.encrypt_instance = encrypt_instance
        self.server_pb_path = ''
        self.server_pk_path = ''
        self.client_pb_path = ''
        self.N = 0
        self.userdict = {'John': (SHA256.new('Smith'),'/pbkey.?')}
        self.session_mac_key=0
        self.session_msg_key=0

    '''used in parse_command'''
    def download_file(self, filename):
        path = self.current_client_dir + filename
        if not os.path.exists(path):
            msg_str = "This file does not exist!"
            msg_bytes = msg_str.encode('ascii')
            self.encrypt_and_send(msg_bytes)    #send err message to client
        else:           #read in file and convert to bytes
            f = open(path, "r")
            msg_str = f.read()      
            msg_bytes = msg_str.encode('ascii')
            f.close()
            self.encrypt_and_send(msg_bytes)    #send file as bytes to client

    '''used in parse_command, encrypts and sends a message to the client'''
    def encrypt_and_send(self, msg_bytes):
        self.encrypt_instance.send(msg_bytes, self.current_client, self.netif)  

    '''This function takes in a decrypted command and executes it, encrypting and sending back a message to the client if necessary'''
    def parse_command(self, plaincomm):     #COMMAND NEEDS TO BE DECRYPTED BEFORE THIS IS CALLED... 
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
                self.encrypt_and_send(msg_bytes)
            else:
                shutil.rmtree(self.current_client_dir + dir_arg, ignore_errors=True)
        elif cmd == "GWD":  #get working directory
            msg_bytes = self.current_client_dir.encode('ascii')
            self.encrypt_and_send(msg_bytes)
        elif cmd == "CWD":  #change directory
            dir_arg = args[1]
            path = self.current_client_dir + dir_arg
            print (path)
            if not os.path.exists(path):    
                msg_str = "This folder does not exist!"
                msg_bytes = msg_str.encode('ascii')
                self.encrypt_and_send(msg_bytes)
            else:
                self.current_client_dir = self.current_client_dir + dir_arg
        elif cmd == "LST": #list contents
            lst = os.listdir(self.current_client_dir)
            msgstr = "\t".join(lst)
            msg_bytes = msgstr.encode('ascii')
            self.encrypt_and_send(msg_bytes)
        elif cmd == "UPL":  #form of upl FILENAME FILECONTENT
            filename = args[1]
            dafile = " ".join(args[2:])
            f = open(self.current_client_dir + filename, "w+")
            f.write(dafile)
            f.close()
        elif cmd == "DNL":  #download file
            self.download_file(args[1])
        elif cmd == "RMF":  #rm file from folder        #in form of "rmf FILE FOLDER"
            os.remove(self.current_client_dir + args[2] + "/" + args[1])   #check formatting
        else:
            msg_str = "Command not found"
            msg_bytes = msg_str.encode('ascii')
            self.encrypt_and_send(msg_bytes)

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




    '''
    Handles login
    '''
    def confirmlogin(msg):
        UID=msg[0:7].decode('utf-8')
        pwd_str=msg[8:15].decode('utf-8')
        if(self.userdict[UID][0]== SHA256.new(pwd_str)): #TODO: BETTER ERROrS CLI
            self.client_public_keypath = self.userdict['UID'][1]
            return True, int.from_bytes(msg[16:32],byteorder='big')
        else:
             print('invalid password recieved')
             return False, 0


    def handle_login():
        netif = network_interface(NET_PATH, OWN_ADDR)
        print('Waiting For Login Attempt')
        status = None
        while (status == None):
        	status, lgn_msg = netif.receive_msg(blocking=True)      # when returns, status is True and msg contains a message

        #deencrypt with the private key.
        lgn_msg_dec = public_key.decrypt(self.private_key_path,lgn_msg)

        #confirm the userid,password pair matches, and return the current_usr_public_key_path
        status,self.N = confirmlogin(lgn_msg_dec)

        #generate the first DH message and secrets X1
        DH1_dict=SessionKeyGenerator.generate_dh1()
        X1 = DH1_dict['X1']
        X2 = DH1_dict['X2']
        DH1_msg = str(DH1_dict['M1'].to_bytes(64,byteorder='big'))+str(DH1_dict['M2'].to_bytes(64,byteorder='big'))+str(DH1_dict['G1'].to_bytes(64,byteorder='big'))+str(DH1_dict['G2'].to_bytes(64,byteorder='big'))+str(DH1_dict['P1'].to_bytes(64,byteorder='big'))+str(DH1_dict['P2'].to_bytes(64,byteorder='big'))

        #sign the message
        DH1_msg_signed = public_key.sign(self.server_pk_path,DH1_msg)

        #append to nonce
        DH1_final_pt = str(self.N.to_bytes(4,byteorder='big')) + DH1_msg_signed
        DH1_final_enc = publickey.encrypt(self.client_pb_path,DH1_final_pt)

        netif.send_msg(self.current_client, DH1_final_enc.encode('utf-8'))

        status = None
        while (status == None):
        	status, msg3_enc = netif.receive_msg(blocking=True)

        msg3_pt_signed= public_key.decrypt(self.client_pk_path,msg3_enc)

        if not (int.from_bytes(msg3_pt_signed[0:3],byteorder='big')==Self.N):
            #Raise an error here that N is not correct
            MA = int.from_bytes(pt_msg2[4:67],byteorder='big')
            MB = int.from_bytes(pt_msg2[68:131],byteorder='big')
            signature = msg3_pt_signed[132:]
        #verify the signature
        if not(public_key.verify(self.server_pb_path,signature)):
            #Raise and error here that the message signature did not verify
            self.session_message_key,self.session_mac_key = SessionKeyGenerator.calculate_keys(MA,MB,X1,X2,DH1_dict['P1'],DH1_dict['P2'])


        return
