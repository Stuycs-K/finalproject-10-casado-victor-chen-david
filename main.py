#!/usr/bin/env python3
import math
import time
import hmac
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
    
    hash = hmac.new(secret_key.to_bytes(numbytes, byteorder='big'),
        flooredtime.to_bytes(8, byteorder='big'), hashlib.sha1).digest()
    print(''.join("{:02x}".format(c) for c in hash))
    with open("buf", "wb") as f:
        f.write(flooredtime.to_bytes(8, byteorder='big'))

    truncated = hash[:4]
    #print(truncated)

    precode = int.from_bytes(truncated, byteorder='big')
    if(precode < 0):
        precode = precode * -1
    #print(precode)

    code = str(precode)
    if len(code) > codelen:
        code = code[:codelen]

    while(len(code) < codelen):
        code = "0" + code

    print(code)
    time.sleep(timestep)
