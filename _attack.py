import _cipher
import _utils

# XOR
def xor_single_byte(ciphertext):
    best_matchness = 0
    for key in range(256):
        plaintext = _cipher.xor_decrypt(ciphertext, chr(key))
        matchness = _utils.frequency_matchness(plaintext)
        if matchness >= best_matchness:
            best_plaintext = plaintext
            best_matchness = matchness
    return (best_plaintext, best_matchness)

def xor_key_length(ciphertext, max_size, number_candidates):
    results = []
    for l in xrange(2, max_size + 1):
        sum_normalized_hamming_distance = 0
        for i in range(5):
            sum_normalized_hamming_distance += _utils.normalized_hamming_distance(ciphertext[i * l : (i + 1) * l], ciphertext[(i + 1) * l : (i + 2) * l])
        results.append([sum_normalized_hamming_distance / 5, l])
    results.sort(key=(lambda result: result[0]))
    results = map(lambda result: result[1], results)
    return results[:number_candidates]

def xor(ciphertext):
    # Estimating a list of key lengths
    candidate_key_lengths = xor_key_length(ciphertext, 40, 5)
    best_matchness = 0
    best_plaintext = ''
    # Guessing the key for each key length
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

# ECB mode detection
def detect_ecb(ciphertext, block_size=16):
    # Not necessarily true.
    block_map = {}
    for l in range(0, len(ciphertext), block_size):
        block = ciphertext[l : l + block_size]
        if block not in block_map:
            block_map[block] = 1
        else:
            return True
    return False