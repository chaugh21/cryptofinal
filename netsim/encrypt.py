from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.Util import Padding
from Crypto import Random


class encrypt:
    
    
    def __init__(self,msg,encrypt_key, mac_key,sqn_number):
        self.msg = msg
        self.encrypt_key = encrypt_key
        self.mac_key = mac_key
        self.sqn_number = sqn_number
    
    def secure_payload(self):
        payload_length = len(self.msg)
        padding_length = AES.block_size - payload_length%AES.block_size
        mac_length = 32  # SHA256 hash value is 32 bytes long
        msg_length = 9 + AES.block_size + payload_length + padding_length + mac_length
        # create header
        header_version = b'\x01\x01'                            # protocol version 1.1
        header_type = b'\x01'                                   # message type 1
        header_length = msg_length.to_bytes(2, byteorder='big') # message length (encoded on 2 bytes)
        header_sqn = (self.sqn_number + 1).to_bytes(4, byteorder='big')  # next message sequence number (encoded on 4 bytes)
        header = header_version + header_type + header_length + header_sqn 

        # pad the payload and encrypt the padded payload with AES in CBC mode using a random iv
        iv = Random.get_random_bytes(AES.block_size)
        ENC = AES.new(self.encrypt_key, AES.MODE_CBC, iv)
        padded_payload = Padding.pad(self.msg, AES.block_size, style='iso7816')
        encrypted_payload = ENC.encrypt(padded_payload)

        # compute the mac on the header, iv, and encrypted payload
        MAC = HMAC.new(self.mac_key, digestmod=SHA256)
        MAC.update(header + iv + encrypted_payload)
        mac = MAC.digest()

        return header + iv + encrypted_payload + mac




