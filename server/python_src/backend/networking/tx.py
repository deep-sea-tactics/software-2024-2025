#pscp  lhs@raspberrypi:ROVCLIENT/rx
#cd /mnt/c/Users/<username>
import os
import sys

if sys.platform != "linux": #pylance will cry here, but this is fine, that's actually intentional
    print("the tx subsystem will not work on your platform, %s" % sys.platform)
    exit()

class Packer:
    def pack():
        os.system("cd server/python_src/backend/networking && cmd.exe /c packer.bat")

if __name__ == "__main__":
    Packer.pack()