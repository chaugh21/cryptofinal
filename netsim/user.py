import Crypto,SessionKeyGenerator,sys
from netinterface import network_interface

class User:

    NET_PATH = './'
    OWN_ADDR = 'A'


    def __init__(self):
        self.N=0
        self.X1 =0
        self.X2=0
        self.server_public_key= ''
        self.usr_private_key=''
        return


    def gen_message1(uid,pwd):
        #create a random nonce N
        self.N = SessionKeyGenerator.genNonce()
        #concat
        msg1_pt = str(uid) + str(pwd)+str(N)
        #enc using the public key of the server. TODO: encode with public key.
        msg1_enc = 'TODO:PKE'(msg1pt)
        return msg1_enc

    def login(self):
        #read in the userid and password from the command line
        print('Welcome to the Secure FTP. Please enter your username').
        userid=str(input())
        #TODO: SELECT THE CORRECT UIDPATH HERE
        print('enter your password')
        pwd_str=str(input())

        #create a message to init the protocol
        enc_msg1 = gen_message1(userid,pwd_str)

        # init the netinterface
        netif = network_interface(NET_PATH,OWN_ADDR)
        #send M1
        netif.send_msg('B', enc_msg.encode('utf-8'))
        status, enc_msg2 = netif.receive_msg(blocking=True)
        if(status):
            pt_msg2= 'TODO: PKE' (enc_msg2, usr_priv_key)
            print('User: Message Recieved From Server:' + str(pt_msg2))
        else:
            #TOOD: RAISE ERROR
            #exit

        
