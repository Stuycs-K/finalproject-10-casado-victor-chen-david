from flask import Flask, render_template, request
from shared.totp import *

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verifyCode', methods=['POST'])
def verify():
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

    codes = [generate_code(secret_key, timestep, codelen), generate_code(secret_key, timestep, codelen, past=1)]
    print(codes)

    if request.method == "POST":
       testcode = request.form.get("code")
       print(testcode)
       if codes[0] == testcode or codes[1] == testcode:
           return ("Code Verified")
       return ("Bad code")
    return ("No code inputted")

if __name__ == '__main__':
    app.run(port = 5001)
