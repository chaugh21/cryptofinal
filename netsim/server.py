import os
import shutil

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
        