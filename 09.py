import _cipher

plaintext_before_pad = 'YELLOW SUBMARINE'
plaintext_after_pad = 'YELLOW SUBMARINE\x04\x04\x04\x04'

assert _cipher.pad(plaintext_before_pad, 20) == plaintext_after_pad