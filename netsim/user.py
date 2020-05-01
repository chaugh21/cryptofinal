import Crypto,SessionKeyGenerator,sys
from netinterface import network_interface
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes

class User:

    NET_PATH = './'
    OWN_ADDR = 'B'


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
        print('Welcome to the Secure FTP. Please enter your username')
        userid=str(input())
        #TODO: SELECT THE CORRECT UIDPATH HERE
        print('enter your password')
        pwd_str=str(input())

        #create a message to init the protocol
        enc_msg1 = gen_message1(userid,pwd_str)

        # init the netinterface
        netif = network_interface(NET_PATH,OWN_ADDR)
        #send M1
        netif.send_msg('A', enc_msg.encode('utf-8'))
        status, enc_msg2 = netif.receive_msg(blocking=True)
        if(status):
            pt_msg2= 'TODO: PKE' (enc_msg2, usr_priv_key)
            print('User: Message Received From Server:' + str(pt_msg2))
        else:
            #TOOD: RAISE ERROR
            #exit
            pass

    '''
    This function is used to generate the derived message and mac keys for
    encrypting individual messages and sends message and mac nonces to the
    server so that it can generate the same keys

    ARGUMENTS:
    session_message_key - bytes: this is the session message key
    session_mac_key - bytes: this is the session mac key
    destination - char: what directory the nonces should be sent to
    network - netinterface: the network interface we are using to send the messages

    RETURNS:
    msg_key - bytes: a 256 byte message key derived from the nonce and session message key
    mac_key - bytes: a 256 byte mac key derived from the nonce and session mac key
    '''
    def client_key_generation(session_message_key, session_mac_key, destination, network):
        msg_nonce = get_random_bytes(256)
        network.send_msg(destination, b'msg'+msg_nonce)
        msg_key = HMAC.new(session_message_key, msg=msg_nonce, digestmod=SHA256).digest()

        mac_nonce = get_random_bytes(256)
        network.send_msg(destination, b'mac'+mac_nonce)
        mac_key = HMAC.new(session_mac_key, msg=mac_nonce, digestmod=SHA256).digest()

        return msg_key, mac_key
