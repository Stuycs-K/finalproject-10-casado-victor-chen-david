from flask import Flask, render_template, request
from main import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verifyCode')
def verify():
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

    code = main.generate_code(secret_key, timestep, codelen)
    print(code)


if __name__ == '__main__':
    app.run(port = 5001)
