import os
import _string
import _cipher

b64_suffix = """
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK
""".strip().replace('\n', '')

suffix = _string.conv(b64_suffix, 'b64')
key = os.urandom(16)
def encryption_oracle(plaintext):
    padded_plaintext = _cipher.pad(plaintext + suffix)
    return _cipher.aes_encrypt(padded_plaintext, key)

def attack():
    # Cracks ECB mode: Obtain fixed_suffix given [payload + fixed_suffix]

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
    suffix_length = len(ciphertext) - block_size - expand_sizes[1]

    # Brute-force the suffix
    """
    1st character:
      |<--------- BLOCK 1 --------->|   |<--------- BLOCK 2 --------->|   |<--------- ...
      |<---------------------- PAYLOAD --------------------->| |<----------- SUFFIX ---------->|
      |<-------- 15 -------->|          |<-------- 15 -------->|
    * [0x00] [0x00] ... [0x00] [????] | [0x00] [0x00] ... [0x00] [s_01] | [s_02] [s_03] ...
      ===============================   =============================== // Check if these two blocks are identical

    2nd character:
      |<--------- BLOCK 1 --------->|   |<--------- BLOCK 2 --------->|   |<--------- ...
      |<------------------- PAYLOAD ------------------->| |<----------- SUFFIX ---------->|
      |<----- 14 ---->|                 |<----- 14 ---->|
    * [0x00] ... [0x00] [s_01] [????] | [0x00] ... [0x00] [s_01] [s_02] | [s_03] [s_04] ...
      ===============================   ===============================

    ...

    15th character:
      |<--------- BLOCK 1 --------->|   |<--------- BLOCK 2 --------->|   |<--------- ...
      |<------------------- PAYLOAD ------------------->| |<----------- SUFFIX ---------->|
    * [0x00] [s_01] ... [s_14] [????] | [0x00] [s_01] ... [s_14] [s_15] | [s_16] [s_17] ...
      ===============================   ===============================

    16th character:
      |<--------- BLOCK 1 --------->|   |<--------- BLOCK 2 --------->|   |<--------- ...
      |<------------------- PAYLOAD ------------------->| |<----------- SUFFIX ---------->|
    * [s_01] [s_12] ... [s_15] [????] | [s_01] [s_02] ... [s_15] [s_16] | [s_17] [s_18] ...
      ===============================   ===============================

    17th character:
      |<--------- BLOCK 1 --------->|   |<--------- BLOCK 2 --------->|   |<--------- BLOCK 3 --------->|   |<--------- ...
      |<----------------------- PAYLOAD ---------------------->| |<------------------------- SUFFIX ----------------------->|
                                        |<-------- 15 -------->|
    * [s_02] [s_03] ... [s_16] [????] | [0x00] [0x00] ... [0x00] [s_01] | [s_02] [s_03] ... [s_16] [s_17] | [s_18] [s_19] ...
      ===============================                                     ===============================

    18th character:
      |<--------- BLOCK 1 --------->|   |<--------- BLOCK 2 --------->|   |<--------- BLOCK 3 --------->|   |<--------- ...
      |<----------------------- PAYLOAD ---------------------->| |<------------------------- SUFFIX ----------------------->|
                                        |<----- 14 ---->|
    * [s_03] [s_04] ... [s_17] [????] | [0x00] ... [0x00] [s_01] [s_02] | [s_03] [s_04] ... [s_17] [s_18] | [s_19] [s_20] ...
      ===============================                                     ===============================
    """
    suffix = ''
    while len(suffix) < suffix_length:
        payload_prefix = ('\x00' * 15 + suffix)[-15:]
        payload_suffix = '\x00' * ((15 - len(suffix)) % 16)
        block = len(suffix) / 16 + 1

        found = False
        for char in range(256):
            payload = payload_prefix + chr(char) + payload_suffix
            ciphertext = encryption_oracle(payload)
            if ciphertext[:16] == ciphertext[block * 16 : (block + 1) * 16]:
                suffix += chr(char)
                found = True
                break
        if found == False:
            suffix += '?'
    return suffix

_suffix = attack()
assert suffix == _suffix
print _suffix