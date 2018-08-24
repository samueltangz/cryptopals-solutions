import _string

hex_string_1 = '1c0111001f010100061a024b53535009181c'
hex_string_2 = '686974207468652062756c6c277320657965'
hex_string_3 = '746865206b696420646f6e277420706c6179'
assert _string.xor(hex_string_1, hex_string_2, 'hex') == hex_string_3
