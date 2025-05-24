import math
import time
from ctypes import *
lib = cdll.LoadLibrary("./shared/hmac_sha1.so");

lib.hmac_sha1.restype = POINTER(c_ubyte)

def hmac_sha1(key: bytes, text: bytes):
    p = lib.hmac_sha1(key, len(key), text, len(text))
    return bytearray(p[:20])

def generate_code(secret, timestep, code_len):
    current_unix_time = time.time()
    flooredtime = math.floor(current_unix_time/timestep)

    if (type(secret) == bytes):
        key = secret
    else:
        numbytes = math.floor((secret_key.bit_length() + 7) / 8)
        key = secret.to_bytes(numbytes, byteorder='big')
    text = flooredtime.to_bytes(8, byteorder='big')
    hash = hmac_sha1(key, text)

    offset = hash[-1] & 15
    truncated = hash[offset:offset + 4]

    precode = int.from_bytes(truncated, byteorder='big') & 2147483647

    code = str(precode % (10 ** code_len))
    if len(code) > code_len:
        code = code[:code_len]

    while(len(code) < code_len):
        code = "0" + code

    return code

def generate_code(secret, timestep, code_len, offset = 0):
    current_unix_time = time.time()
    flooredtime = math.floor(current_unix_time/timestep)
    flooredtime -= offset

    if (type(secret) == bytes):
        key = secret
    else:
        numbytes = math.floor((secret.bit_length() + 7) / 8)
        key = secret.to_bytes(numbytes, byteorder='big')
    text = flooredtime.to_bytes(8, byteorder='big')

    hash = hmac_sha1(key, text)

    offset = hash[-1] & 15
    truncated = hash[offset:offset + 4]

    precode = int.from_bytes(truncated, byteorder='big') & 2147483647

    code = str(precode % (10 ** code_len))
    if len(code) > code_len:
        code = code[:code_len]

    while(len(code) < code_len):
        code = "0" + code

    return code
