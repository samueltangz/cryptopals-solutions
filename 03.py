import _attack
import _string

hex_ciphertext = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
ciphertext = _string.conv(hex_ciphertext, 'hex')

best_plaintext, best_matchness = _attack.xor_single_byte(ciphertext)

print '%s [Matchness: %f]' % (best_plaintext, best_matchness)