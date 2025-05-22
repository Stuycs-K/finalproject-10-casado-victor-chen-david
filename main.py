#!/usr/bin/env python3
import math
import time
import hmac
from hmac_custom import hmac_sha1
import hashlib
import subprocess
from sys import argv
from urllib.parse import urlparse

timestep = 30
codelen = 8
secret_key = 0xAAAA0000AAAAAAABABB

def generate_code(secret, timestep, code_len):
    current_unix_time = time.time()
    flooredtime = math.floor(current_unix_time/timestep)
    numbytes = math.floor((secret_key.bit_length() + 7) / 8)

    key = secret_key.to_bytes(numbytes, byteorder='big')
    text = flooredtime.to_bytes(8, byteorder='big')
    hash = hmac_sha1(key, text)

    offset = hash[-1] & 15
    truncated = hash[offset:offset + 4]

    precode = int.from_bytes(truncated, byteorder='big') & 2147483647

    code = str(precode % (10 ** codelen))
    if len(code) > codelen:
        code = code[:codelen]

    while(len(code) < codelen):
        code = "0" + code

    return code

# https://github.com/google/google-authenticator/wiki/Key-Uri-Format
if len(argv) > 1:
    print(argv[1])
    url = urlparse(argv[1])
    if (url.scheme != "otpauth"):
        print("INVALID URL!")

while(True):
    print(generate_code(secret_key, timestep, codelen))
    time.sleep(timestep)
