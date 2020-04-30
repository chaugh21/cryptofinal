
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.Util import Padding
from Crypto import Random


class decrypt:
    def __init__(self,msg,encrypt_key,mac_key,rcvsqn):
        self.msg = msg
        self.encrypt_key = encrypt_key
        self.mac_key = mac_key
        self.rcvsqn = rcvsqn

    def decrypt_msg(self):
        header = self.msg[0:9]                              # header is 9 bytes long
        iv = self.msg[9:9+AES.block_size]                   # iv is AES.block_size bytes long
        mac = self.msg[-32:]                                # last 32 bytes is the mac
        encrypted_payload = self.msg[9+AES.block_size:-32]  # encrypted payload is between iv and mac
        header_version = header[0:2]                   # version is encoded on 2 bytes 
        header_type = header[2:3]                      # type is encoded on 1 byte 
        header_length = header[3:5]                    # msg length is encoded on 2 bytes 
        header_sqn = header[5:9]    


        if len(self.msg) != int.from_bytes(header_length,byteorder='big'):
            return "Warning: Message length value in header is wrong!"

        snd_number = int.from_bytes(header_sqn, byteorder='big')
        if snd_number - self.rcvsqn != 1:
            return print("Error: Message sequence number is too old!")
        else:
            self.rcvsqn = self.rcvsqn + 1

        MAC = HMAC.new(self.mac_key, digestmod=SHA256)
        MAC.update(header + iv + encrypted_payload)
        computed_mac = MAC.digest() 
        if (computed_mac != mac):
            return "Error: MAC verification failed!"
       
        ENC = AES.new(self.encrypt_key, AES.MODE_CBC, iv)
        try:
            padded_payload = ENC.decrypt(encrypted_payload)
            payload = Padding.unpad(padded_payload, AES.block_size, style='iso7816')
        except Exception as e:
            return "Error: Decryption failed!"
   

        return payload.decode('utf-8')
