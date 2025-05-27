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
    codes = [generate_code(secret_key, timestep, codelen), generate_code(secret_key, timestep, codelen, offset=1)]
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
