import _string
from Crypto.Cipher import AES

# XOR
def xor_encrypt(plaintext, key):
    key = key * (len(plaintext) / len(key)) + key[0 : len(plaintext) % len(key)]
    return _string.xor(plaintext, key)

def xor_decrypt(ciphertext, key):
    # Encryption with xor == decryption with xor
    return xor_encrypt(ciphertext, key)

# AES
def _aes_cipher(key, mode, iv):
    if mode == 'ECB':
        return AES.new(key, AES.MODE_ECB)
    elif mode == 'CBC':
        return AES.new(key, AES.MODE_CBC, iv)
    else:
        raise ModeNotImplementedError(mode)    

def aes_encrypt(plaintext, key, mode='ECB', iv=None):
    cipher = _aes_cipher(key, mode, iv)
    return cipher.encrypt(plaintext)

def aes_decrypt(ciphertext, key, mode='ECB', iv=None):
    cipher = _aes_cipher(key, mode, iv)
    return cipher.decrypt(ciphertext)

# Block cipher padding
def pad(plaintext, block_size=16, scheme='PKCS#7'):
    if scheme == 'PKCS#7':
        pad = block_size - len(plaintext) % block_size
        return plaintext + pad * chr(pad)
    else:
        raise SchemeNotImplementedError(scheme)

def unpad(plaintext, block_size=16, scheme='PKCS#7'):
    if scheme == 'PKCS#7':
        pad = ord(plaintext[-1])
        if pad == 0 or plaintext[-pad:] != pad * chr(pad):
            raise PaddingInvalidError(plaintext)
        return plaintext[:-pad]
    else:
        raise SchemeNotImplementedError(scheme)

# Exceptions
class ModeNotImplementedError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class SchemeNotImplementedError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PaddingInvalidError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)