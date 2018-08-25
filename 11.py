import random
import os
import _cipher
import _attack

def _random_string(length):
    return os.urandom(length)
def encryption_oracle(plaintext):
    prefix_length = random.randint(5, 10)
    suffix_length = random.randint(5, 10)
    mode_id = random.randint(0, 1)
    key = _random_string(16)
    iv = _random_string(16)
    padded_plaintext = _cipher.pad(
        _random_string(prefix_length) + plaintext + _random_string(suffix_length)
    )
    if mode_id == 0:
        mode = 'ECB'
    else:
        mode = 'CBC'
    return _cipher.aes_encrypt(padded_plaintext, key, mode, iv), mode

for test in xrange(1000):
    ciphertext, mode = encryption_oracle('*' * 64)
    if _attack.detect_ecb(ciphertext):
        _mode = 'ECB'
    else:
        _mode = 'CBC'
    assert mode == _mode