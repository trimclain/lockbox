#!/usr/bin/env python3

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encrypt_to_file(file: str, passphrase: str) -> None:
    """
    Read the data from a file, encrypt it and write back to the file

    Args:
        file: path to a file
        passphrase: used to create the Fernet key
    """
    with open(file, 'r') as f:
        data = f.read()
    token = encrypt(data, passphrase)
    with open(file, 'wb') as f:
        f.write(token)


def encrypt(data: str, passphrase: str) -> bytes:
    """
    Encrypt a string and return it

    Args:
        data: to be encrypted
        passphrase: used to create the Fernet key

    Returns:
        token: a Fernet token with encrypted data

    Raises:
        None
    """
    passphrase_bytes = passphrase.encode()   # convert string to bytes

    # salt = os.urandom(16)
    # TODO: Gotta figure out how to properly store this so I can decrypt
    salt = b'\x10\x1b\xddJ\xb2\xcd\xd5\x9bD\xc5\x93\xa4\xb9\xb6)\xce'
    kdf = PBKDF2HMAC(   # Password Based Key Derivation Function 2 HMAC
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(passphrase_bytes))

    f = Fernet(key)

    token = f.encrypt(data.encode())
    return token


if __name__ == "__main__":
    data = "BigSecretThing"
    passphrase = "Testing"
    print(encrypt(data, passphrase)) # b'gAAAAABkkRi4yHq2FiRVu9Ou0mMuiMaIv2MNOYiq3ia0jzM_7x2mbz839k-7cXlzUAjRntJy0_8AkzTw2Q1Y1T0U18-4M2A6xw=='
