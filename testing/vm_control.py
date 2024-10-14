import subprocess
import data as dt

def start_vm(vm_name:str, soft:str):
    try:
        if soft == "vb":
            subprocess.run([dt.VBOXMANAGE_PATH,
                            "startvm",
                            vm_name,
                            "--type",
                            "headless"],
                           check=True,
                           capture_output=subprocess.DEVNULL,
                           text=subprocess.DEVNULL)
        elif soft == "vmware":
            subprocess.run([dt.VMRUN_PATH,
                            "start",
                            dt.data_vm[soft][vm_name][2],
                            "nogui"],
                           check=True,
                           capture_output=subprocess.DEVNULL,
                           text=subprocess.DEVNULL)
    except Exception as e:
        print(e)

def run_on_vm(vm_name:str, soft:str, exe_guest_path:str)->subprocess.CompletedProcess:
    try:
        username = dt.data_vm[soft][vm_name][0]
        password = dt.data_vm[soft][vm_name][1]
        if soft == "vb":
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
        elif soft == "vmware":
            return subprocess.run([
                dt.VMRUN_PATH,
                "-gu", username,
                "-gp", password,
                "runProgramInGuest",
                dt.data_vm[soft][vm_name][2],
                exe_guest_path
            ], capture_output=True, text=True)

    except Exception as e:
        print(e)

def savestate_vm(vm_name:str, soft:str):
    try:
        if soft == "vb":
            subprocess.run([dt.VBOXMANAGE_PATH,
                            "controlvm",
                            vm_name,
                            "savestate"],
                           check=True,
                           capture_output=subprocess.DEVNULL,
                           text=subprocess.DEVNULL)
        elif soft == "vmware":
            subprocess.run([dt.VMRUN_PATH,
                            "suspend",
                            dt.data_vm[soft][vm_name][2]],
                           check=True,
                           capture_output=subprocess.DEVNULL,
                           text=subprocess.DEVNULL)
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
        elif soft == "vmware":
            return subprocess.run([
                dt.VMRUN_PATH,
                "-gu", username,
                "-gp", password,
                "CopyFileFromHostToGuest",
                dt.data_vm[soft][vm_name][2],
                host_path, guest_path
            ], capture_output=True, text=True)
    except Exception as e:
        print(e)