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
    """Generates an RSA keypair"""
    run_command(["openssl", "genpkey", "-algorithm", "RSA", "-out", "private_key.pem", "-pkeyopt", "rsa_keygen_bits:2048"])
    run_command(["openssl", "rsa", "-pubout", "-in", "private_key.pem", "-out", "public_key.pem"])


def encrypt(in_file:str):
    """Encrypts a file using openssl

    Args:
        in_file (str): The file to be encrypted (use small files)
    """
    run_command(["openssl", "rsautl", "-encrypt", "-inkey", "public_key.pem", "-pubin", "-in", in_file, "-out", in_file.replace(".txt",".enc")])


def decrypt(in_file:str):
    """Decrypts a file using openssl

    Args:
        in_file (str): The file to be decrypted
    """
    run_command(["openssl", "rsautl", "-decrypt", "-inkey", "private_key.pem", "-in", in_file, "-out", in_file.replace(".enc", ".dec")])


def ec_sign(in_file:str):
    """A function to sign files using openssl

    Args:
        in_file (str): the file to sign
    """
    run_command(["openssl", "dgst", "-sha256", "-sign", "private_key.pem", "-out", in_file + ".sig", in_file])


def ec_verify(in_file:str):
    """A function to verify a signature using openssl

    Args:
        in_file (str): File to verify
    """
    result = run_command(["openssl", "dgst", "-sha256", "-verify", "public_key.pem", "-signature", in_file.replace(".dec",".txt") + ".sig", in_file])

    with open("./verified.txt", "w") as file:
        file.write(result)


def main():
    if not is_tool("openssl"):
        print("Install openssl to continue")
        exit()

    with open("./example.txt", "w") as plaintext:
        plaintext.write("Example Text")

    gen_keypair()

    ec_sign("./example.txt")
    encrypt("./example.txt")
    decrypt("./example.enc")
    ec_verify("./example.dec")

if __name__ == "__main__":
    main()