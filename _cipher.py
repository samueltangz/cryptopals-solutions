import _string

def xor_cipher_encrypt(plaintext, key, type=None):
    if type != None:
        return _string.conv(
            xor_cipher_encrypt(_string.conv(plaintext, type), _string.conv(key, type)),
            None, type
        )
    key = key * (len(plaintext) / len(key)) + key[0 : len(plaintext) % len(key)]
    return _string.xor(plaintext, key)

def xor_cipher_decrypt(ciphertext, key, type=None):
    # Encryption with xor == decryption with xor
    return xor_cipher_encrypt(ciphertext, key, type)
