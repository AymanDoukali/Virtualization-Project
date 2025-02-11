# Automated Virtualization Detection Project

This project is dedicated to exploring and evaluating several methods for detecting virtualization environments.
The project provides an automated framework to evaluate different virtualization detection methods using Python test scripts and pre-compiled executables.


## Project Overview

- **Detection Methods**: The source files `m1.c` through `m5.c` reside in `src/m/`, and their pre-compiled executables are placed in `src/exe/`.
- **Configuration**:  
  - A single YAML file, `config.yaml`, holds VM information (e.g., credentials, paths) and logging settings.  
  - Methods (m1...m5) are listed here with their descriptions.
- **VirtualMachine Module**:  
  - `VirtualMachine.py` defines classes (`VBVM` for VirtualBox, `VMwareVM` for VMware) handling VM actions such as start, copy files, and execute commands.
- **Test Scripts**:  
  - `test_m.py` runs one or more detection methods on a specified VM or the current physical machine.  
  - `test_all.py` runs methods on all configured VMs, optionally generating a JSON report of results (`test_result.json`).

## Key Sections in `config.yaml`

- **Constants**
  - `DELAY`: Specifies the delay (in seconds) applied after a virtual machine has started.

- **Logging Configuration**

- **File Paths**
  - `EXE_PATH`: Directory where the executable files for the detection methods reside (It is not recommended to change this path).
  - `VBOXMANAGE_PATH` & `VMRUN_PATH`: Paths to the VirtualBox and VMware management executables. These may need to be updated to reflect your installation directories.

- **Virtual Machine (VM) Configuration**
  - **VirtualBox (vb)** and **VMware (vmware)**: Define the VMs available for testing. For each VM, you need to specify:
    - Operating system (`os`): Options include `"win"`, `"linux"`, or `"mac"`.
    - Administrator username (`user`) and password (`password`).
    - For VMware VMs, provide the path to the corresponding `.vmx` file.
  
- **Methods to be Tested**
  - The section `m` defines the detection methods (m1 through m5) along with brief descriptions.
  - **Important**: To test a method, ensure that:
    - The executable file for the method has the same name as the method identifier (e.g., `m1`, `m2`, etc.).
    - The executable is located in the directory specified by `EXE_PATH`.


## Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/AymanDoukali/Virtualization-Project.git
   cd your-repository-directory
   
2. **Update the config.yaml file**  
Instructions are to be found in the previous section or in the config.yaml file.

3. **Set Up VMs**  
   Make sure your virtual machines are correctly referenced in `config.yaml` with valid credentials and paths.

4. **Run Tests**  
   - Call functions like `test_m_on_all_vm(m, result_dict)` or `test_all_m_on_all_vm()` (in `test_all.py`) to run executables on all VMs.  
   - Or use `test_m_vm(m, vm_instance)` (in `test_m.py`) to test a single method on one VM.

5. **Logging & Results**  
   - Logs are written to both the console and `app.log` (as configured in `config.yaml`).  
   - Bulk test outcomes are saved in `test_result.json`.


#
For additional details or troubleshooting information, see the comments and docstrings in the Python scripts.