from netinterface import network_interface
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes

'''
This function is used to generate the derived message and mac keys for encrypting individual messages and sends message and mac nonces to the server so that it can generate the same keys

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
