#include <stdio.h>
#include <string.h>

// Inline assembly is used to invoke the CPUID instruction
void cpuid(int code, unsigned int *a, unsigned int *b, unsigned int *c, unsigned int *d)
{
  __asm__ volatile("cpuid"
                   : "=a"(*a), "=b"(*b), "=c"(*c), "=d"(*d)
                   : "a"(code), "c"(0));
}

// Function to check for virtualization using the CPUID instruction
int is_physical_machine()
{
  unsigned int eax, ebx, ecx, edx;

  // CPUID with EAX=1: Standard Feature Flags
  cpuid(1, &eax, &ebx, &ecx, &edx);

  // Bit 31 of ECX indicates if a hypervisor is present
  if (ecx & (1 << 31))
  {
    // CPUID with EAX=0x40000000: Hypervisor Present
    cpuid(0x40000000, &eax, &ebx, &ecx, &edx);

    // Extract the hypervisor signature from EBX, ECX, and EDX
    char hypervisor_signature[13];
    memcpy(hypervisor_signature, &ebx, 4);
    memcpy(hypervisor_signature + 4, &ecx, 4);
    memcpy(hypervisor_signature + 8, &edx, 4);
    hypervisor_signature[12] = '\0';

    printf("Detected Hypervisor Signature: %s\n", hypervisor_signature);

    // Return 0, indicating a virtual machine
    return 0;
  }

  // Return 1, indicating a physical machine
  return 1;
}

int main()
{
  if (is_physical_machine())
  {
    printf("The program is running on a physical machine.\n");
    return 1;
  }
  else
  {
    printf("The program is running on a virtual machine.\n");
    return 0;
  }
}
