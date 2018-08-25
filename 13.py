import os
import _cipher

# === Preparation ===
def parse(payload):
    obj = {}
    params = payload.split('&')
    for param in params:
        k, v = param.split('=')
        obj[k] = v
    return obj

assert parse('foo=bar&baz=qux&zap=zazzle') == {'foo': 'bar', 'baz': 'qux', 'zap': 'zazzle'}

def profile_for(email):
    # Sanitize
    email = email.replace('&', '').replace('=', '')
    return 'email=%s&uid=10&role=user' % email

assert profile_for('foo@bar.com') == 'email=foo@bar.com&uid=10&role=user'

key = os.urandom(16)
def encrypt_profile(email):
    plaintext = _cipher.pad(profile_for(email))
    return _cipher.aes_encrypt(plaintext, key, 'ECB')

def decrypt_profile(ciphertext):
    plaintext = _cipher.unpad(_cipher.aes_decrypt(ciphertext, key, 'ECB'))
    return parse(plaintext)

def validate(ciphertext):
    obj = decrypt_profile(ciphertext)
    return 'role' in obj and obj['role'] == 'admin'

# === Challenge ===
# Goal: Use only encrypt_profile() to generate a ciphertext such that
#   validate(ciphertext) == True

# Ciphertext is the following plaintext encrypted (padded)
# email=13chars@a.admin[\x0b * 11]com&uid=10&role=user[ \x0a * 10]
# |<-- Block 1 ->||<-- Block 2 ->||<-- Block 3 ->||<-- Block 4 ->|
ciphertext = encrypt_profile('13chars@a.' + 'admin' + '\x0b' * 11 + 'com')

# Desired plaintext
# email=13chars@a.com&uid=10&role=admin[\x0b * 11]
# |<-- Block 1 ->||<-- Block 3 ->||<-- Block 2 ->|
forged_ciphertext = ciphertext[0:16] + ciphertext[32:48] + ciphertext[16:32]

print decrypt_profile(forged_ciphertext)

# Goal test
assert validate(forged_ciphertext) == True
