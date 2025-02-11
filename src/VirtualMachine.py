from abc import ABC, abstractmethod
import subprocess
import yaml

# Load the YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    

class VirtualMachine(ABC):
    def __init__(self, name, soft, user, password, os):
        self.name = name
        self.soft = soft
        self.user = user
        self.password = password
        self.os = os
    def __str__(self):
        return f"{self.name} ({self.os}) {self.soft}"

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def save_state(self):
        pass

    @abstractmethod
    def copy_to_vm(self, host_path, guest_path):
        pass
    
    @abstractmethod
    def run_on_vm(self, exe_guest_path):
        pass

class VBVM(VirtualMachine):
    def __init__(self, name, user, password, os):
        super().__init__(name, "vb", user, password, os)

    def start(self):
        try:
            subprocess.run([config['paths']['VBOXMANAGE_PATH'],
                            "startvm",
                            self.name,
                            "--type",
                            "headless"],
                           check=True,
                           capture_output=subprocess.DEVNULL,
                           text=subprocess.DEVNULL)
        except Exception as e:
            print(e)
    
    def save_state(self):
        try:
            subprocess.run([config['paths']['VBOXMANAGE_PATH'],
                            "controlvm",
                            self.name,
                            "savestate"],
                           check=True,
                           capture_output=subprocess.DEVNULL,
                           text=subprocess.DEVNULL)
        except Exception as e:
            print(e)

    def copy_to_vm(self, host_path, guest_path):
        try:
            subprocess.run([config['paths']['VBOXMANAGE_PATH'],
                            "guestcontrol",
                            self.name,
                            "copyto",
                            host_path,
                            guest_path,
                            "--username",
                            self.user,
                            "--password",
                            self.password],
                           check=True)
        except Exception as e:
            print(e)
            
    def run_on_vm(self, exe_guest_path:str) -> subprocess.CompletedProcess:
        try:
            username = config['vm']['vb'][self.name]["user"]
            password = config['vm']['vb'][self.name]["password"]
            return subprocess.run([
                config['paths']['VBOXMANAGE_PATH'],
                "guestcontrol",
                self.name, "run",
                "--exe",
                exe_guest_path,
                "--username",
                username,
                "--password",
                password
            ], capture_output=True, text=True)
        except Exception as e:
            print(e)

class VMwareVM(VirtualMachine):
    def __init__(self, name, user, password, os, path):
        super().__init__(name, "vmware", user, password, os)
        self.path = path

    def start(self):
        try:
            subprocess.run([config['paths']['VMRUN_PATH'],
                            "start",
                            self.path,
                            "nogui"],
                           check=True,
                           capture_output=subprocess.DEVNULL,
                           text=subprocess.DEVNULL)
        except Exception as e:
            print(e)

    def save_state(self):
        try:
            subprocess.run([config['paths']['VMRUN_PATH'],
                            "suspend",
                            self.path],
                           check=True,
                           capture_output=subprocess.DEVNULL,
                           text=subprocess.DEVNULL)
        except Exception as e:
            print(e)

    def copy_to_vm(self, host_path, guest_path):
        try:
            subprocess.run([
                config['paths']['VMRUN_PATH'],
                "-gu", self.user,
                "-gp", self.password,
                "CopyFileFromHostToGuest",
                self.path,
                host_path, guest_path
                ], capture_output=True, text=True)
        except Exception as e:
            print(e)

    def run_on_vm(self, exe_guest_path):
        try:
            username = config['vm']['vmware'][self.name]["user"]
            password = config['vm']['vmware'][self.name]["password"]
            return subprocess.run([
                config['paths']['VMRUN_PATH'],
                "-gu", username,
                "-gp", password,
                "runProgramInGuest",
                config['vm']['vmware'][self.name]["path"],
                exe_guest_path
                ], capture_output=True, text=True)
        except Exception as e:
            print(e)