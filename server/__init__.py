from flask import Flask, render_template, request, flash, redirect, url_for
from shared.totp import *

app = Flask(__name__)

app.secret_key = 'the random string'

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
           flash ("Code Verified")
       else:
           flash ("Bad Code")
    else:
       flash("No code inputted")
    return redirect('/')

if __name__ == '__main__':
    app.run(port = 5001)
