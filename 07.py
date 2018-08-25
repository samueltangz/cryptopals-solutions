import _string
import _cipher

f = open('source/7.txt')
b64_ciphertext = f.read()
f.close()

ciphertext = _string.conv(b64_ciphertext, 'b64')

print _cipher.aes_decrypt(ciphertext, 'YELLOW SUBMARINE')