import base64

def conv(payload, from_type=None, to_type=None):
    if from_type == 'hex':
        return conv(payload.decode('hex'), None, to_type)
    elif from_type == 'b64':
        return conv(base64.b64decode(payload), None, to_type)
    elif from_type != None:
        raise TypeNotImplementedError(from_type)
    if to_type == 'hex':
        return payload.encode('hex')
    elif to_type == 'b64':
        return base64.b64encode(payload)
    elif to_type == None:
        return payload
    else:
        raise TypeNotImplementedError(to_type)

def xor(payload_1, payload_2, type=None):
    if type != None:
        return conv(
            xor( 
                conv(payload_1, type),
                conv(payload_2, type)
            ),
            None,
            type)
    return ''.join([chr(ord(u) ^ ord(v)) for u, v in zip(payload_1, payload_2)])

# Errors
class TypeNotImplementedError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)