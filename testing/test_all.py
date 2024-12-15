from VirtualMachine import VirtualMachine, VMwareVM, VBVM
from test_m import test_m_vm, test_m_pm
import yaml
import logging.config
import json

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Apply the logging configuration
logging.config.dictConfig(config)
logger = logging.getLogger('test_logger')


def get_vm() -> list[VirtualMachine]:
    """
    get_vm loads all available virtual machines from the config file
    :return: a list of available virtual machines
    """
    logger.info('Getting Virtual Machines data from the config file')
    vm_list = []
    for soft in config['vm'].keys():
        logger.debug(f'soft = {soft}')
        for vm_name in config['vm'][soft].keys():
            logger.debug(f'soft = {soft} / vm_name = {vm_name}')
            try:
                if soft == 'vb':
                    vm = VBVM(vm_name, soft, config['vm'][soft][vm_name]['user'],
                              config['vm'][soft][vm_name]['password'])
                elif soft == 'vmware':
                    vm = VMwareVM(vm_name, soft, config['vm'][soft][vm_name]['user'],
                                  config['vm'][soft][vm_name]['password'], config['vm'][soft][vm_name]['path'])
            except Exception as e:
                logger.error(f'Wrong Machine config : soft = {soft} / vm_name = {vm_name}')
                logger.debug(e)

            vm_list.append(vm)
    return vm_list

def test_m_on_all_vm(m:str, d:dict):
    """
    this function tests method m on all virtual machines in config['vm'].
    It shows all tests results in the console
    :param m: method to test
    :return:
    """
    vm_list = get_vm()
    for vm in vm_list:
        output = test_m_vm(m, vm)
        if output > 0:
            # data_test[soft][vm].append(m)
            d[m].append((vm.soft, vm.name))
            logger.info(f"\n\tTesting {m} on {vm.name} ({vm.soft}) = Success ({output})\n")
            # if m not in config['vm'][soft][vm]["m"]:
            #    config['vm'][soft][vm]["m"].append(m)
        else:
            logger.error(f"\n\tTesting {m} on {vm.name} ({vm.soft}) = Failure {output}\n")

def test_all():
    """
    This function tests every method in config['m'] on all virtual machines in config['vm'].
    It saves all tests results in the test_result.json file.
    """
    logger.info("Tests begin")
    data_test = {}
    for m in config['m'].keys():
        data_test[m] = []
        output_pm = test_m_pm(m)
        if output_pm == 0:
            logger.info(f"\n\tTesting {m} on real machine = Success ({output_pm})\n")
        else:
            logger.info(f"\n\tTesting {m} on real machine = Failure {output_pm}\n")

        test_m_on_all_vm(m, data_test)

        # Writing JSON data to a file
        with open('test_result.json', 'w') as json_file:
            json.dump(data_test, json_file, indent=4)


test_all()
