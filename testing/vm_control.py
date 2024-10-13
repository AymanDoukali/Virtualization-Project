import subprocess
import data as dt

def start_vm(vm_name:str, soft:str):
    try:
        if soft == "vb":
            subprocess.run([dt.VBOXMANAGE_PATH, "startvm", vm_name, "--type", "headless"],
                                  check=True, capture_output=subprocess.DEVNULL, text=subprocess.DEVNULL)
    except Exception as e:
        print(e)

def run_on_vm(vm_name:str, soft:str, exe_guest_path:str)->subprocess.CompletedProcess:
    try:
        if soft == "vb":
            username = dt.data_vm[soft][vm_name][0]
            password = dt.data_vm[soft][vm_name][1]
            return subprocess.run([
                dt.VBOXMANAGE_PATH,
                "guestcontrol",
                vm_name, "run",
                "--exe",
                exe_guest_path,
                "--username",
                username,
                "--password",
                password
            ], capture_output=True, text=True)
    except Exception as e:
        print(e)

def savestate_vm(vm_name:str, soft:str):
    try:
        if soft == "vb":
            subprocess.run([dt.VBOXMANAGE_PATH, "controlvm", vm_name, "savestate"],
                          check=True, capture_output=subprocess.DEVNULL, text=subprocess.DEVNULL)
    except Exception as e:
        print(e)

def copy_to_vm(vm_name:str, soft:str, host_path:str, guest_path:str):
    try:
        username = dt.data_vm[soft][vm_name][0]
        password = dt.data_vm[soft][vm_name][1]
        if soft == "vb":
            subprocess.run([dt.VBOXMANAGE_PATH,
                                   "guestcontrol",
                                   vm_name,
                                   "copyto",
                                   host_path,
                                   guest_path,
                                   "--username",
                                   username,
                                   "--password",
                                   password],
                                  check=True)
    except Exception as e:
        print(e)