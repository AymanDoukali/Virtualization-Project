#include <stdio.h>
#include <windows.h>
#include <string.h>

// Function to check if a system value indicates a virtual machine
int is_suspicious_value(const char *value)
{
  if (strstr(value, "VMware") || strstr(value, "VirtualBox") || (strstr(value, "VBOX")) ||
      strstr(value, "Hyper-V") || strstr(value, "Xen") ||
      strstr(value, "KVM") || strstr(value, "QEMU"))
  {
    return 0;
  }
  return 1;
}

int check_virtual_machine()
{
  HKEY hKey;
  DWORD index = 0;
  char valueName[256];
  DWORD valueNameSize;
  BYTE valueData[1024];
  DWORD valueDataSize;
  DWORD type;

  // Open the "System" registry key
  if (RegOpenKeyEx(HKEY_LOCAL_MACHINE, "HARDWARE\\DESCRIPTION\\System", 0, KEY_READ, &hKey) == ERROR_SUCCESS)
  {
    printf("Opened System registry key. Checking values...\n");

    // Enumerate all values under the key
    while (1)
    {
      valueNameSize = sizeof(valueName);
      valueDataSize = sizeof(valueData);

      // Read the next value
      if (RegEnumValue(hKey, index, valueName, &valueNameSize, NULL, &type, valueData, &valueDataSize) == ERROR_SUCCESS)
      {
        // Print the value name
        printf("Value #%d: %s = ", index + 1, valueName);

        // Check if the value is of string type (REG_SZ)
        if (type == REG_SZ || type == REG_MULTI_SZ)
        {
          printf("%s\n", (char *)valueData);

          // Check if the value is suspicious
          if (is_suspicious_value((char *)valueData))
          {
            RegCloseKey(hKey);
            return 0; // Return 0 if suspicious value is found
          }
        }
        else if (type == REG_DWORD)
        {
          DWORD dwordValue = *(DWORD *)valueData;
          printf("%lu (DWORD)\n", dwordValue);
        }
        else
        {
          printf("Type not supported\n");
        }

        index++;
      }
      else
      {
        break; // No more values to read
      }
    }
    RegCloseKey(hKey);
  }
  else
  {
    printf("Error opening System registry key.\n");
  }

  index = 0;

  if (RegOpenKeyEx(HKEY_LOCAL_MACHINE, "HARDWARE\\DESCRIPTION\\System\\BIOS", 0, KEY_READ, &hKey) == ERROR_SUCCESS)
  {
    printf("\nOpened System\\BIOS registry key. Checking values...\n");

    // Enumerate all values under the key
    while (1)
    {
      valueNameSize = sizeof(valueName);
      valueDataSize = sizeof(valueData);

      // Read the next value
      if (RegEnumValue(hKey, index, valueName, &valueNameSize, NULL, &type, valueData, &valueDataSize) == ERROR_SUCCESS)
      {
        // Print the value name
        printf("Value #%d: %s = ", index + 1, valueName);

        // Check if the value is of string type (REG_SZ)
        if (type == REG_SZ || type == REG_MULTI_SZ)
        {
          printf("%s\n", (char *)valueData);

          // Check if the value is suspicious
          if (is_suspicious_value((char *)valueData))
          {
            RegCloseKey(hKey);
            return 0; // Return 0 if suspicious value is found
          }
        }
        else if (type == REG_DWORD)
        {
          DWORD dwordValue = *(DWORD *)valueData;
          printf("%lu (DWORD)\n", dwordValue);
        }
        else
        {
          printf("Type not supported\n");
        }

        index++;
      }
      else
      {
        break; // No more values to read
      }
    }
    RegCloseKey(hKey);
  }
  else
  {
    printf("Error opening System registry key.\n");
  }

  return 1; // Return 1 if no suspicious values were found
}

int main()
{
  int result = check_virtual_machine();

  if (result == 0)
  {
    printf("\nresult:\nSuspicious value found. This may be a virtual machine.\n");
  }
  else
  {
    printf("\nresult:\nNo suspicious values found. This is likely a physical machine.\n");
  }

  return result;
}
