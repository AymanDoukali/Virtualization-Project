#include <stdio.h>
#include <stdint.h>

// Function to read the timestamp counter using RDTSCP
static inline uint64_t rdtscp()
{
    uint32_t eax, edx;
    __asm__ volatile("rdtscp" : "=a"(eax), "=d"(edx) : : "ecx");
    return ((uint64_t)edx << 32) | eax;
}

// Function to execute CPUID
void cpuid(uint32_t leaf, uint32_t *eax, uint32_t *ebx, uint32_t *ecx, uint32_t *edx)
{
    __asm__ volatile(
        "cpuid"
        : "=a"(*eax), "=b"(*ebx), "=c"(*ecx), "=d"(*edx)
        : "a"(leaf));
}

int main()
{
    uint64_t start, end;
    uint32_t eax, ebx, ecx, edx;
    int iterations = 10000;
    double total_cycles = 0.0;

    // Measure time taken for multiple CPUID executions
    for (int i = 0; i < iterations; i++)
    {
        start = rdtscp(); // Timestamp before CPUID
        cpuid(0, &eax, &ebx, &ecx, &edx);
        end = rdtscp(); // Timestamp after CPUID
        total_cycles += (end - start);
    }

    double average_cycles = total_cycles / iterations;
    printf("Average CPUID execution cycles: %.2f\n", average_cycles);

    // Virtualization detection threshold
    if (average_cycles > 10000)
    { // Adjust the threshold based on your environment
        printf("THIS IS A VIRTUAL MACHINE.\n");
        return 0;
    }
    else
    {
        printf("No virtualization detected.\n");
        return 1;
    }
}
