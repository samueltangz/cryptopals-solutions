import os
import random
import _string
import _cipher

prefix = os.urandom(random.randint(64, 127))
suffix = os.urandom(random.randint(64, 127))
key = os.urandom(16)
def encryption_oracle(plaintext):
    padded_plaintext = _cipher.pad(prefix + plaintext + suffix)
    return _cipher.aes_encrypt(padded_plaintext, key)

def _common_prefix(ciphertexts, block_size):
    prefix_length = 0
    while True:
        if ciphertexts[0][prefix_length : prefix_length + block_size] == ciphertexts[1][prefix_length : prefix_length + block_size]:
            prefix_length += block_size
        else:
            return prefix_length

def attack():
    # Cracks ECB mode: Obtain fixed_suffix given [fixed_prefix + payload + fixed_suffix]

    # Get block size and length of suffix
    expand_sizes = []
    plaintext_length = 0
    old_ciphertext = encryption_oracle('')
    while len(expand_sizes) < 2:
        plaintext_length += 1
        ciphertext = encryption_oracle('A' * plaintext_length)
        if len(ciphertext) > len(old_ciphertext):
            expand_sizes.append(plaintext_length)
        old_ciphertext = ciphertext

    block_size = expand_sizes[1] - expand_sizes[0]
    total_length = len(ciphertext) - block_size - expand_sizes[1]

    ciphertexts = []
    ciphertexts.append(encryption_oracle(''))
    ciphertexts.append(encryption_oracle('A'))
    ciphertexts.append(encryption_oracle('AA'))
    plaintext_length = 2
    while _common_prefix(ciphertexts[0:2], block_size) == _common_prefix(ciphertexts[1:3], block_size):
        plaintext_length += 1
        ciphertexts.append(encryption_oracle('A' * plaintext_length))
        ciphertexts = ciphertexts[1:]
    prefix_length = _common_prefix(ciphertexts[1:3], block_size) - plaintext_length + 1
    suffix_length = total_length - prefix_length

    # Brute-force the suffix
    """
    1st character:
      |<--------- BLOCK 1 --------->|   |<--------- BLOCK 2 --------->|   |<--------- BLOCK 3 --------->|   |<--------- BLOCK 4 --------->|   |<--------- ...
      |<---------------- PREFIX ---------------->| |<---------------------------------- PAYLOAD ---------------------------------->| |<-------- SUFFIX ------>|
    * [p_01] [p_02] [p_03] ... [p_16] | [p_17] ... [0x00] [0x00] [0x00] | [0x00] ... [0x00] [0x00] [????] | [0x00] ... [0x00] [0x00] [s_01] | [s_02] [s_03] ...
                                                                          ===============================   =============================== // Check if these two blocks are identical
    """
    suffix = ''
    while len(suffix) < suffix_length:
        payload_prefix = '\x00' * (-prefix_length % 16) + ('\x00' * 15 + suffix)[-15:]
        payload_suffix = '\x00' * ((15 - len(suffix)) % 16)
        block_first = (prefix_length + 15) / 16
        block_check = (prefix_length + 15) / 16 + len(suffix) / 16 + 1

        found = False
        for char in range(256):
            payload = payload_prefix + chr(char) + payload_suffix
            ciphertext = encryption_oracle(payload)
            if ciphertext[block_first * 16 : (block_first + 1) * 16] == ciphertext[block_check * 16 : (block_check + 1) * 16]:
                suffix += chr(char)
                found = True
                break
        if found == False:
            suffix += '?'
    return suffix

_suffix = attack()
assert suffix == _suffix
