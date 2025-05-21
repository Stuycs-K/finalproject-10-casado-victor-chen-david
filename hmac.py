from ctypes import *
lib = cdll.LoadLibrary("./hmac_src/hmac_sha.so");

text = b'hello'
key = b'key'

lib.hmac_sha1.restype = POINTER(c_ubyte)

p = lib.hmac_sha1(text, len(text), key, len(key))
b = bytearray(p[:20])

print(''.join(format(x, '02x') for x in b))
