#include <stdio.h>
#include <stdint.h>
#include <unistd.h>

// Function to read the timestamp counter
static inline uint64_t rdtscp()
{
    uint32_t eax, edx;
    __asm__ volatile("rdtscp" : "=a"(eax), "=d"(edx) : : "ecx");
    return ((uint64_t)edx << 32) | eax;
}

int main()
{
    uint64_t start, end;
    int iterations = 10000;
    double total_cycles = 0.0;

    // Measure time taken for a simple system call (getpid)
    for (int i = 0; i < iterations; i++)
    {
        start = rdtscp();
        getpid(); // Simple system call
        end = rdtscp();
        total_cycles += (end - start);
    }

    double average_cycles = total_cycles / iterations;
    printf("Average getpid() execution cycles: %.2f\n", average_cycles);

    // Virtualization detection threshold
    if (average_cycles > 65)
    { // Adjust threshold based on tests
        printf("Detected virtualization (linux vm or vmware suspend).\n");
        return 0;
    }
    else
    {
        printf("No virtualization detected.\n");
        return 1;
    }
}
