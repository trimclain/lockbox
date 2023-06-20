#!/usr/bin/env python3

import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def decrypt_from_file(file: str, passphrase: str) -> str:
    """
    Decrypt the token from a file

    Args:
        file: path to a file
        passphrase: used to create the Fernet key

    Returns:
        Decrypted data or None
    """
    with open(file, 'rb') as f:
        token = f.read()
    return decrypt(token, passphrase)


def decrypt(token: bytes, passphrase: str) -> str:
    """
    Read an encrypted data from a file and decrypt it

    Args:
        token: encrypted data
        passphrase: used to create the Fernet key

    Returns:
        Decrypted data or a warning message

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

    try:
        data = f.decrypt(token)
        return data.decode()
    except InvalidToken:
        return 'Wrong passphrase! Try again'


if __name__ == "__main__":
    data = b'gAAAAABkkRib_8jE3UTB13_CpefhipOnl08ORy0A0dXJg_mt_tc6Ac19B0201utR45c_rkXWW4j8jbcskZMt_A24icdInTu_hA=='
    passphrase = "Testing"
    print(decrypt(data, passphrase)) # BigSecretThing
