import _string
import _attack

f = open('source/8.txt')
hex_ciphertexts = f.read().strip().split('\n')
f.close()

for hex_ciphertext in hex_ciphertexts:
    ciphertext = _string.conv(hex_ciphertext, 'hex')
    if _attack.detect_ecb(ciphertext):
        print hex_ciphertext