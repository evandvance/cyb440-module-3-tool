import subprocess
from shutil import which

MASTERPASSWORD:str = "cryptography"

def is_tool(name:str) -> bool:
    """A function to check if a command line tool is installed

    Args:
        name (str): Name of the command line tool to check for

    Returns:
        bool: If the command line tool is installed the function returns True.
    """
    return which(name) is not None


def run_command(command:list[str]) -> str:
    """Run a command in the shell environment

    Args:
        command (list[str]): The command broken up into a list of strings by word.

    Raises:
        RuntimeError: If the command fails in some way it will end the program and print the commands error on the console

    Returns:
        str: The commands command line output
    """
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if output.returncode != 0:
        raise RuntimeError(output.stderr.decode("utf-8"))

    return output.stdout.decode("utf-8").strip()


def gen_keypair():
    pass


def encrypt():
    pass


def decrypt():
    pass


def ec_sign():
    pass


def ec_verify():
    pass


def main():
    pass

if __name__ == "__main__":
    main()