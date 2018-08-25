import _string
import _cipher

f = open('source/10.txt')
ciphertext = _string.conv(f.read(), 'b64')

def challenge_aes_decrypt(ciphertext, key, iv):
    # The decrypt method for this challenge.
    # Expected to have the same plaintext from AES-CBC mode.
    plaintext = ''
    last_ciphertext_block = iv
    for l in range(0, len(ciphertext), 16):
        ciphertext_block = ciphertext[l : l + 16]
        plaintext += _string.xor(
            _cipher.aes_decrypt(ciphertext_block, key, 'ECB'),
            last_ciphertext_block
        )
        last_ciphertext_block = ciphertext_block
    return plaintext

plaintext = _cipher.aes_decrypt(ciphertext, 'YELLOW SUBMARINE', 'CBC', '\x00' * 16)
_plaintext = challenge_aes_decrypt(ciphertext, 'YELLOW SUBMARINE', '\x00' * 16)

assert plaintext == _plaintext
print _plaintext