import _string
import _cipher
import _utils

# XOR
def xor_single_byte(ciphertext, type=None):
    if type != None:
        return xor_single_byte(_string.conv(ciphertext, type))
    best_matchness = 0
    for key in range(256):
        plaintext = _cipher.xor_cipher_decrypt(ciphertext, chr(key))
        matchness = _utils.frequency_matchness(plaintext)
        if matchness >= best_matchness:
            best_plaintext = plaintext
            best_matchness = matchness
    return (best_plaintext, best_matchness)

def xor_key_length(ciphertext, max_size, number_candidates, type=None):
    if type != None:
        return xor_key_length(_string.conv(ciphertext, type), max_size, candidates)
    results = []
    for l in xrange(2, max_size + 1):
        sum_normalized_hamming_distance = 0
        for i in range(5):
            sum_normalized_hamming_distance += _utils.normalized_hamming_distance(ciphertext[i * l : (i + 1) * l], ciphertext[(i + 1) * l : (i + 2) * l])
        results.append([sum_normalized_hamming_distance / 5, l])
    results.sort(key=(lambda result: result[0]))
    results = map(lambda result: result[1], results)
    return results[:number_candidates]

def xor(ciphertext, type=None):
    if type != None:
        return xor(_string.conv(ciphertext, type))

    candidate_key_lengths = xor_key_length(ciphertext, 40, 5)
    best_matchness = 0
    best_plaintext = ''
    for key_length in candidate_key_lengths:
        grouped_ciphertexts = [''] * key_length
        grouped_plaintexts = [''] * key_length
        for ind in range(len(ciphertext)):
            grouped_ciphertexts[ind % key_length] += ciphertext[ind]
        for ind in xrange(key_length):
            grouped_plaintexts[ind], matchness = xor_single_byte(grouped_ciphertexts[ind])
        plaintext = ''
        for ind in range(len(ciphertext)):
            plaintext += grouped_plaintexts[ind % key_length][ind / key_length]
        matchness = _utils.frequency_matchness(plaintext)
        if matchness > best_matchness:
            best_plaintext = plaintext
            best_matchness = matchness
    return best_plaintext