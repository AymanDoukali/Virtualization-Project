from os.path import abspath
import yaml
import subprocess
import time
import logging.config
from VirtualMachine import VirtualMachine, VMwareVM

# Load the YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Apply the logging configuration
logging.config.dictConfig(config)
logger = logging.getLogger('test_logger')


def test_m_vm(m: str, vm: VirtualMachine) -> int:
    """
    test_m_vm runs the method m on the virtual machine vm
    :param m: method to test
    :param vm: virtual machine to test
    :return: 0 if physical machine, 1 if virtual machine
    """
    print(f"Testing method {m} on virtual machine {vm.name} ({vm.soft})\n")
    logger.info(f"Testing method {m} on virtual machine {vm.name} ({vm.soft})\n")
    try:
        # Starting the virtual machine
        logger.info("Starting virtual machine...")
        vm.start()
        # Waiting for the virtual machine to completely starts
        time.sleep(config['consts']['DELAY'])
        # Copying exe to the vm
        logger.info("Copying executable to virtual machine...")
        EXE_FULL_PATH = abspath(config['paths']['EXE_PATH']) + "\\"
        host_path = f"{EXE_FULL_PATH}{m}.exe"
        guest_path = f"C:\\Users\\{config['vm'][vm.soft][vm.name]['user']}\\Desktop\\{m}.exe"
        vm.copy_to_vm(host_path, guest_path)
        # Running the exe on the vm
        logger.info("Running executable on virtual machine...")
        output = vm.run_on_vm(guest_path)
        logger.debug(output.stdout)
        # Saving the vm state
        logger.info("Saving virtual machine state...\n")
        vm.save_state()
        return output.returncode
    except Exception as e:
        logger.error(e)


def test_m_pm(m:str) -> int:
    """
    test_m_pm runs the method on the current machine
    :param m: method to test
    :return: 0 if physical machine, 1 if virtual machine
    """
    logger.info(f"Testing method {m} on this machine:\n")
    print(f"Testing method {m} on this machine:\n")
    try:
        output = subprocess.run([config['paths']["EXE_PATH"] + m + ".exe"], capture_output=True, text=True)
        logger.debug(output.stdout)
        return output.returncode
    except Exception as e:
        logger.error(e)