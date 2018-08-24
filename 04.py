import _attack

f = open('source/4.txt')
hex_ciphertexts = f.read().strip().split('\n')
f.close()

best_matchness = 0
for hex_ciphertext in hex_ciphertexts:
    plaintext, matchness = _attack.xor_single_byte(hex_ciphertext, 'hex')
    if matchness >= best_matchness:
        best_plaintext = plaintext
        best_matchness = matchness

print '%s [Matchness: %f]' % (best_plaintext, best_matchness)