from os.path import abspath

data_vm = {
    "vb": {
        "Win7": ["user", "password"],
        "Win8": ["vbox", "changeme"],
        "WinXP": []
    },
    "vmware": {
        "Win8":["adkh", "password", "D:\\8.Virtual Machines\\win 8 vmware\\Windows 8.x x64.vmx"]
    }
}


EXE_PATH = "../exe/"
EXE_FULL_PATH = abspath(EXE_PATH) + "\\"
GUEST_PATH = "C:\\Users\\"#user\\Desktop\\"
VBOXMANAGE_PATH = "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe"
VMRUN_PATH = "C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe"
