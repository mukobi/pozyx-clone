import pip  # needed to use the pip functions
import time
import sys

if __name__ == "__main__":
    time.sleep(0.1)
    print("Version:")
    time.sleep(0.1)
    print(sys.version)
    time.sleep(0.1)
    print(" ")
    time.sleep(0.1)
    print("Version Info:")
    time.sleep(0.1)
    print(sys.version_info)
    time.sleep(0.1)
    print("-")

    print("Installed modules:")
    for i in pip.get_installed_distributions(local_only=True):
        print(i)
        time.sleep(0.1)

    print("-")
    time.sleep(0.1)
    print("Python Path Location:")
    time.sleep(0.1)
    print(sys.path)
    time.sleep(0.1)