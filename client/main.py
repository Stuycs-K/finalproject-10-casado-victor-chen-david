from sys import argv
from urllib.parse import urlparse,parse_qs, unquote
import base64
from shared.totp import *

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
    if "secret" in q:
        secret_key = base64.b32decode(q["secret"][0])
    if "period" in q:
        timestep = int(q["period"][0])
    if "algorithm" in q:
        if q["algorithm"][0] != "SHA1":
            # we could also support alternative algorithms but we have yet to find examples to use, apparently Google Authenticator used to ignore this flag outright
            print("INVALID ALGORITHM")
    if "digits" in q:
        codelen = int(q["digits"][0])

while(True):
    print(generate_code(secret_key, timestep, codelen))
    time.sleep(time.time() % timestep)
