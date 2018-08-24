import _string
import _cipher
import _utils

plaintext = """
Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal
""".strip()
key = 'ICE'
hex_ciphertext = _string.conv(_cipher.xor_cipher_encrypt(plaintext, key), None, 'hex')

expected_hex_ciphertext = """
0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f
""".replace('\n', '')

assert hex_ciphertext == expected_hex_ciphertext