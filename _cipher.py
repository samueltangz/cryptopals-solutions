import _string
from Crypto.Cipher import AES

def xor_encrypt(plaintext, key):
    key = key * (len(plaintext) / len(key)) + key[0 : len(plaintext) % len(key)]
    return _string.xor(plaintext, key)

def xor_decrypt(ciphertext, key):
    # Encryption with xor == decryption with xor
    return xor_encrypt(ciphertext, key)

def aes_cipher(key, mode):
    if mode == 'ECB':
        return AES.new(key, AES.MODE_ECB)
    else:
        raise ModeNotImplementedError(mode)    

def aes_encrypt(plaintext, key, iv=None, mode='ECB'):
    cipher = aes_cipher(key, mode)
    return cipher.encrypt(plaintext)

def aes_decrypt(ciphertext, key, iv=None, mode='ECB'):
    cipher = aes_cipher(key, mode)
    return cipher.decrypt(ciphertext)

# Exceptions
class ModeNotImplementedError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)