import _attack
import _utils
import _string

assert _utils.hamming_distance('this is a test', 'wokka wokka!!!') == 37

f = open('source/6.txt')
b64_ciphertext = f.read().replace('\n', '')
f.close()

ciphertext = _string.conv(b64_ciphertext, 'b64')

print _attack.xor(ciphertext)