from ctypes import *
lib = cdll.LoadLibrary("./hmac_src/hmac_sha.so");

lib.hmac_sha1.restype = POINTER(c_ubyte)

def hmac_sha1(key: bytes, text: bytes):
    p = lib.hmac_sha1(key, len(key), text, len(text))
    return bytearray(p[:20])
