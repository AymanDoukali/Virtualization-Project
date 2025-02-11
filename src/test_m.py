import os
import yaml
import subprocess
import time
import logging.config
from src.VirtualMachine import VirtualMachine

# Load configuration from YAML file
CONFIG_PATH = 'config.yaml'
with open(CONFIG_PATH, 'r') as file:
    config = yaml.safe_load(file)

# Apply logging configuration
logging.config.dictConfig(config)
logger = logging.getLogger('test_logger')


def get_executable_paths(m: str, vm: VirtualMachine) -> tuple[str, str]:
    """
    Determines the appropriate host and guest paths for the executable based on the VM's OS.
    :param m: Method name (executable identifier)
    :param vm: Virtual machine instance
    :return: Tuple containing (host_path, guest_path)
    """
    exe_full_path = os.path.abspath(config['paths']['EXE_PATH'])

    if vm.os == "win":
        host_path = f"{exe_full_path}\\{m}.exe"
        guest_path = f"C:\\Users\\{config['vm'][vm.soft][vm.name]['user']}\\Desktop\\{m}.exe"
    elif vm.os == "linux":
        host_path = f"{exe_full_path}/{m}.out"
        guest_path = f"/home/{vm.user}/Desktop/{m}.out"
    else:
        logger.fatal("Unsupported virtual machine OS or incorrect configuration.")
        return "", ""

    return host_path, guest_path


def test_m_vm(m: str, vm: VirtualMachine) -> int:
    """
    Runs a specified method (executable) on a virtual machine and determines if virtualization is detected.
    :param m: Method to test (name of the executable)
    :param vm: Virtual machine instance
    :return: 1 if a physical machine is detected, 0 if a virtual machine is detected
    """
    logger.info(f"Testing method {m} on virtual machine {vm.name} ({vm.soft})")

    try:
        logger.info("Starting virtual machine...")
        vm.start()
        time.sleep(config['consts']['DELAY'])  # Wait for VM to start completely

        host_path, guest_path = get_executable_paths(m, vm)
        if not host_path or not guest_path:
            return -1  # Indicating an error in configuration

        logger.info("Copying executable to virtual machine...")
        vm.copy_to_vm(host_path, guest_path)

        logger.info("Running executable on virtual machine...")
        output = vm.run_on_vm(guest_path)
        logger.debug(output.stdout)

        logger.info("Saving virtual machine state...")
        vm.save_state()

        return output.returncode
    except Exception as e:
        logger.error(f"Error while testing {m} on VM: {e}")
        return -1


def test_m_list_vm(m_list: list[str], vm: VirtualMachine) -> list[str]:
    """
    Runs multiple methods (executables) on a virtual machine and returns those that detected virtualization.
    :param m_list: List of methods to test
    :param vm: Virtual machine instance
    :return: List of methods that detected virtualization (return code 0)
    """
    logger.info(f"Testing methods {m_list} on virtual machine {vm.name} ({vm.soft})")
    detected_methods = []

    try:
        logger.info("Starting virtual machine...")
        vm.start()
        time.sleep(config['consts']['DELAY'])  # Ensure VM is fully started

        for m in m_list:
            logger.info(f"Copying and running {m} on virtual machine...")
            host_path, guest_path = get_executable_paths(m, vm)
            if not host_path or not guest_path:
                continue

            vm.copy_to_vm(host_path, guest_path)
            output = vm.run_on_vm(guest_path)
            logger.debug(output.stdout)

            if output.returncode == 0:
                logger.info(f"{m} detected virtualization on {vm.name} ({vm.soft})")
                detected_methods.append(m)
            else:
                logger.info(f"{m} did not detect virtualization on {vm.name} ({vm.soft})")

        logger.info("Saving virtual machine state...")
        vm.save_state()

    except Exception as e:
        logger.error(f"Error while testing methods on VM: {e}")

    return detected_methods


def test_m_current(m: str) -> int:
    """
    Runs a specified method (executable) on the current physical machine.
    :param m: Method to test (name of the executable)
    :return: 0 if a physical machine is detected, 1 if a virtual machine is detected
    """
    logger.info(f"Testing method {m} on the current machine")
    try:
        exe_path = os.path.join(config['paths']['EXE_PATH'], f"{m}.exe")
        output = subprocess.run([exe_path], capture_output=True, text=True)
        logger.debug(output.stdout)
        return output.returncode
    except Exception as e:
        logger.error(f"Error while testing {m} on the physical machine: {e}")
        return -1
