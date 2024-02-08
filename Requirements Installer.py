import subprocess
import os

def install_requirements():
    requirements = [
        "PyQt5",
        "requests",
        "beautifulsoup4",
        "pywin32",
    ]

    for requirement in requirements:
        try:
            subprocess.check_call(["pip", "install", requirement])
        except subprocess.CalledProcessError as e:
            print(f"Error installing {requirement}: {e}")
            input("Press Enter to exit")
            return

    # Check if all requirements are installed successfully
    all_installed = all(subprocess.call(["pip", "show", requirement], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0 for requirement in requirements)

    # If all requirements are installed successfully, delete the script
    if all_installed:
        os.remove(__file__)

if __name__ == "__main__":
    install_requirements()
