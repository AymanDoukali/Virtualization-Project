from os.path import abspath

data_vm = {
    "vb": {
        "Win7": ["user", "password"],
        "Win8": ["vbox", "changeme"],
        "WinXP": []
    },
    "vmware": {
        "Win 8"
    }
}


EXE_PATH = "../exe/"
EXE_FULL_PATH = abspath(EXE_PATH) + "\\"
GUEST_PATH = "C:\\Users\\user\\Desktop\\"
VBOXMANAGE_PATH = "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe"
