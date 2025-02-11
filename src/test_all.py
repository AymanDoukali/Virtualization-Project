import yaml
import logging.config
import json
from src.VirtualMachine import VirtualMachine, VMwareVM, VBVM
from src.test_m import test_m_vm, test_m_current, test_m_list_vm

# Load configuration from YAML file
CONFIG_PATH = 'config.yaml'
with open(CONFIG_PATH, 'r') as file:
    config = yaml.safe_load(file)

# Apply logging configuration
logging.config.dictConfig(config)
logger = logging.getLogger('test_logger')


def get_vm() -> list[VirtualMachine]:
    """
    Loads all available virtual machines from the config file.
    :return: List of available virtual machines.
    """
    logger.info('Loading virtual machines from configuration')
    vm_list = []

    for soft, vm_data in config['vm'].items():
        for vm_name, details in vm_data.items():
            try:
                if soft == 'vb':
                    vm = VBVM(vm_name, details['user'], details['password'], details['os'])
                elif soft == 'vmware':
                    vm = VMwareVM(vm_name, details['user'], details['password'], details['os'], details['path'])
                vm_list.append(vm)
            except Exception as e:
                logger.error(f'Invalid configuration for {soft} / {vm_name}: {e}')

    return vm_list


def get_m() -> list[str]:
    """
    Loads all available methods from the config file.
    :return: List of available methods.
    """
    logger.info('Loading methods from configuration')
    return list(config.get('m', {}).keys())


def test_m_on_all_vm(m: str, d: dict):
    """
    Tests a method on all configured virtual machines.
    :param m: Method to test.
    :param d: Dictionary storing test results.
    """
    for vm in get_vm():
        output = test_m_vm(m, vm)
        if output > 0:
            d[m].append((vm.soft, vm.name))
            logger.info(f"Testing {m} on {vm.name} ({vm.soft}) = Success ({output})")
        else:
            logger.error(f"Testing {m} on {vm.name} ({vm.soft}) = Failure ({output})")


def test_all_m_on_all_vm():
    """
    Tests all configured methods on all virtual machines, saving results to a file.
    """
    logger.info('Starting tests for all methods on all virtual machines')
    data_test = {m: [] for m in get_m()}

    for vm in get_vm():
        for m in test_m_list_vm(get_m(), vm):
            data_test[m].append((vm.soft, vm.name))

    with open('test_result.json', 'w') as json_file:
        json.dump(data_test, json_file, indent=4)


def test_all():
    """
    Tests all methods on both the real and virtual machines, saving results to a file.
    """
    logger.info("Starting comprehensive tests on all systems")
    data_test = {m: [] for m in config.get('m', {})}

    for m in data_test.keys():
        output_pm = test_m_current(m)
        logger.info(f"Testing {m} on real machine = {'Success' if output_pm == 1 else 'Failure'} ({output_pm})")
        test_m_on_all_vm(m, data_test)

    with open('test_result.json', 'w') as json_file:
        json.dump(data_test, json_file, indent=4)

# test_all_m_on_all_vm()
