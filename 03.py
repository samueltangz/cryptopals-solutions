import _attack

hex_ciphertext = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

best_plaintext, best_matchness = _attack.xor_single_byte(hex_ciphertext, 'hex')

print '%s [Matchness: %f]' % (best_plaintext, best_matchness)