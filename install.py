import os
import subprocess


def install_pipreqs():
    current_working_directory = os.getcwd()

    subprocess.run(["pip", "install", "pipreqs"])
    print("pipreqs installed.\n")
    subprocess.run(["pipreqs", current_working_directory])
    print("pipreqs generated requirements.txt.\n")


if __name__ == "__main__":
    install_pipreqs()
