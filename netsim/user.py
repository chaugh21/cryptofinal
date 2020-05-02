import Crypto,SessionKeyGenerator,sys
from netinterface import network_interface
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes

class User:

    NET_PATH = './'         #should this be ./NETWORK ?????
    OWN_ADDR = 'B'


    def __init__(self):
        self.N=0
        self.X1 =0
        self.X2=0
        self.server_public_key= ''
        self.usr_private_key=''
        self.userid = ''
        self.session_msg_key=0
        self.session_mac_key=0
        return


    def gen_message1(uid,pwd):
        #create a random nonce N
        self.N = SessionKeyGenerator.genNonce()
        #concat
        msg1_pt = str(uid.to_bytes(8,byteorder='big')) + str(pwd.to_bytes(8,byteorder='big'))+str(self.N.to_bytes(4,byteorder='big'))
        #enc using the public key of the server. TODO: encode with public key.
        msg1_enc = PublicKey.encrypt(self.server_public_key,msg1_pt)
        return msg1_enc

    def login():
        #read in the userid and password from the command line
        print('Welcome to the Secure FTP. Please enter your username')
        self.userid=str(input())
        print('enter your password')
        pwd_str=str(input())

        #create a message to init the protocol
        enc_msg1 = gen_message1(self.userid,pwd_str)

        # init the netinterface
        netif = network_interface(NET_PATH,OWN_ADDR)
        #send M1
        netif.send_msg('A', enc_msg.encode('utf-8'))

        #Wait for M2
        while (status == None):
            status, enc_msg2 = netif.receive_msg(blocking=True)

        #TODO: HANDLE ERRORS
        pt_msg2= publickey.decrypt(self.client_pk_path,enc_msg2)
        print('User: Message Received From Server:' + str(pt_msg2))
        if not (int.from_bytes(pt_msg2[0:3],byteorder='big')==Self.N):
            #Raise an error here that N is not correct

        signature = pt_msg2[388:]
        #verify the signature
        if not (public_key.verify(self.server_pb_path,signature)):
            #Raise and error here that the message signature did not verify

        M1 = int.from_bytes(pt_msg2[4:67],byteorder='big')
        M2 = int.from_bytes(pt_msg2[68:131],byteorder='big')
        G1 = int.from_bytes(pt_msg2[132:195],byteorder='big')
        G2 = int.from_bytes(pt_msg2[196:259],byteorder='big')
        P1 = int.from_bytes(pt_msg2[260:323],byteorder='big')
        P2 = int.from_bytes(pt_msg2[324:387],byteorder='big')

        DH2 = SessionKeyGenerator.generate_dh2(G1,G2,P1,P2)
        self.session_message_key,self.session_mac_key = SessionKeyGenerator.calculate_keys(M1,M2,DH2['Y1'],DH2['Y2'],P1,P2)
        print(session_message_key,session_mac_key)

        #create+sign+encode+send msg3
        msg3_pt = str(self.N.to_bytes(4,byteorder='big')) + str(DH2['M1'].to_bytes(64,byteorder='big')) +str(DH2['M2'].to_bytes(64,byteorder='big')))
        msg3_pt_signed = publickey.sign(self.client_pk_path,msg3_pt)
        msg3_enc = public_key.encrypt(self.server_public_key,msg3_pt_signed)
        netif.send_msg('A', msg3_enc.encode('utf-8'))

        return


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
