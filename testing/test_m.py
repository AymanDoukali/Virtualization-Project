import data as dt
import vm_control as vm
import subprocess
import time


def test_m_vm(m: str, soft: str, vm_name: str, detail: bool=True) -> int:
    """
    test_m_vm runs the method on a virtual machine
    :param m: method to test
    :param soft: virtualization software
    :param vm_name: virtual machine name
    :param detail: detailed output
    :return: 0 if physical machine, 1 if virtual machine
    """
    print(f"Testing method {m} on virtual machine {vm_name} ({soft})\n")
    try:
        # Starting the virtual machine
        if detail:
            print("Starting virtual machine...")
        vm.start_vm(vm_name, soft)
        # Waiting for the virtual machine to completely starts
        time.sleep(30)
        # Copying exe to the vm
        if detail:
            print("Copying executable to virtual machine...")
        host_path = f"{dt.EXE_FULL_PATH}{m}.exe"
        guest_path = f"{dt.GUEST_PATH}{m}.exe"
        vm.copy_to_vm(vm_name, soft, host_path, guest_path)
        # Running the exe on the vm
        if detail:
            print("Running executable on virtual machine...")
        output = vm.run_on_vm(vm_name, soft, guest_path)
        if detail:
            print(output.stdout)
        # Saving the vm state
        if detail:
            print("Saving virtual machine state...")
        vm.savestate_vm(vm_name, soft)
        return output.returncode
    except Exception as e:
        print(e)


# print(test_m_vm("m1", "vmware", "Win8", detail=True))


def test_m_pm(m:str, detail:bool) -> int:
    """
    test_m_pm runs the method on the current machine
    :param m: method to test
    :param detail: detailed output
    :return: 0 if physical machine, 1 if virtual machine
    """
    print(f"Testing method {m} on this machine:\n")
    try:
        output = subprocess.run([dt.EXE_PATH + m + ".exe"], capture_output=True, text=True)
        if detail:
            print(output.stdout)
        return output.returncode
    except Exception as e:
        print(e)

# print(test_m_pm("m1", False))