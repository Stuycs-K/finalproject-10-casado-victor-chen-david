#!/usr/bin/env python3
import math
import time
import hmac
#from hmac_custom import hmac_sha1
import hashlib
import subprocess
from sys import argv
from urllib.parse import urlparse,parse_qs, unquote
import base64

def generate_code(secret, timestep, code_len, past = 0):
    current_unix_time = time.time()
    flooredtime = math.floor(current_unix_time/timestep)
    flooredtime -= past

    if (type(secret) == bytes):
        key = secret
    else:
        numbytes = math.floor((secret.bit_length() + 7) / 8)
        key = secret.to_bytes(numbytes, byteorder='big')
    text = flooredtime.to_bytes(8, byteorder='big')

    hash = hmac.new(key,text, hashlib.sha1).digest()
    #hash = hmac_sha1(key, text)

    offset = hash[-1] & 15
    truncated = hash[offset:offset + 4]

    precode = int.from_bytes(truncated, byteorder='big') & 2147483647

    code = str(precode % (10 ** code_len))
    if len(code) > code_len:
        code = code[:code_len]

    while(len(code) < code_len):
        code = "0" + code

    return code

if __name__ == '__main__':

    timestep = 30
    # RFC 6238 uses 8 in its example implementation, no explicit recommendations; Google defaults to 6 and that appears to be standard everywhere else
    codelen = 6
    secret_key = 0xAAAA0000AAAAAAABABB

    # https://github.com/google/google-authenticator/wiki/Key-Uri-Format
    if len(argv) > 1:
        url = urlparse(argv[1])
        if (url.scheme != "otpauth"):
            print("INVALID URL!")
        if (url.netloc != "totp"):
            # HOTP could be supported if we wanted to but we do not have any good examples to test with
            print("INVALID OTP TYPE!")
        if (url.path):
            print(unquote(url.path.strip("/")))
        q = parse_qs(url.query)
        if q["secret"]:
            secret_key = base64.b32decode(q["secret"][0])
        if q["period"]:
            timestep = int(q["period"][0])
        if q["algorithm"]:
            if q["algorithm"][0] != "SHA1":
                # we could also support alternative algorithms but we have yet to find examples to use, apparently Google Authenticator used to ignore this flag outright
                print("INVALID ALGORITHM")
        if q["digits"]:
            codelen = int(q["digits"][0])

    while(True):
        print(generate_code(secret_key, timestep, codelen))
        time.sleep(time.time() % timestep)
