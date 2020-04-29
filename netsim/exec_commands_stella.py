import os
import shutil

"""LIST OF COMMANDS
MKD FOLDER
RMD FOLDER
GWD
CWD FOLDER
LST FOLDER
UPL FILE
DNL FILE
RMF FILE, FOLDER"""

PATH = "./"         #what path should this be? we need server folder for user

#server
def parse_command(plaincomm, dst):
    args = plaincomm.split()
    cmd = (args[0]).upper()
    if cmd == "MKD":
        new_dir = PATH + args[1] #excludes space
        os.mkdir(new_dir)
        return  #do we want to give result?
    elif cmd == "RMD":
        dir_arg = args[1]
        if not os.path.exists(PATH + dir_arg):
            print ("This folder does not exist!")
        else:
            shutil.rmtree(PATH + dir_arg, ignore_errors=True)
        return
    elif cmd == "GWD":
        return os.getcwd() #check
    elif cmd == "CWD":
        os.chdir(PATH + args[1])  #check if this is allowed and if it exists
        return
    elif cmd == "LST":
        return os.listdir() #type list
    elif cmd == "UPL":
        upload_file(args[1], dst)    #do this
        return
    elif cmd == "DNL":
        download_file(args[1], dst)
        return
    elif cmd == "RMF":
        os.remove(PATH + args[2] + "/" + args[1])   #check formatting
        return
    else:
        return "Command not found"
