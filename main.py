#!/usr/bin/env python3
import math
import time
import hmac
from hmac_custom import hmac_sha1
import hashlib
import subprocess

timestep = 30
codelen = 8
secret_key = 0xAAAA0000AAAAAAABABB
print(secret_key.to_bytes(64, byteorder='big'));

while(True):
    current_unix_time = time.time()
    flooredtime = math.floor(current_unix_time/timestep)
    #print(flooredtime)
    #print(secret_key)
    numbytes = math.floor((secret_key.bit_length() + 7) / 8)

    key = secret_key.to_bytes(numbytes, byteorder='big')
    text = flooredtime.to_bytes(8, byteorder='big')
    print(''.join("{:02x}".format(c) for c in key))
    print(''.join("{:02x}".format(c) for c in text))
    print("original")
    hash = hmac.new(key, text, hashlib.sha1).digest()
    print(''.join("{:02x}".format(c) for c in hash))
    print("custom")
    hash = hmac_sha1(key, text)
    print(''.join("{:02x}".format(c) for c in hash))
    #with open("buf", "wb") as f:
    #    f.write(flooredtime.to_bytes(8, byteorder='big'))

    offset = hash[-1] & 15
    truncated = hash[offset:offset + 4]
    #print(truncated)

    precode = int.from_bytes(truncated, byteorder='big') & 2147483647
    #print(precode)

    code = str(precode % (10 ** codelen))
    if len(code) > codelen:
        code = code[:codelen]

    while(len(code) < codelen):
        code = "0" + code

    print(code)
    time.sleep(timestep)
