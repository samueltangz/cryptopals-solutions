import _cipher

assert _cipher.unpad('ICE ICE BABY\x04\x04\x04\x04') == 'ICE ICE BABY'

try:
  _cipher.unpad('ICE ICE BABY\x05\x05\x05\x05')
  assert False, 'Should throw exception'
except _cipher.PaddingInvalidError:
  pass

try:
  _cipher.unpad('ICE ICE BABY\x01\x02\x03\x04')
  assert False, 'Should throw exception'
except _cipher.PaddingInvalidError:
  pass
  