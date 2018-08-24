import _attack
import _utils

assert _utils.hamming_distance('this is a test', 'wokka wokka!!!') == 37

f = open('source/6.txt')
ciphertext = f.read().replace('\n', '')
f.close()

print _attack.xor(ciphertext, 'b64')