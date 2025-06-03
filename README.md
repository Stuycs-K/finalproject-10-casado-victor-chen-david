[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/am3xLbu5)
# Temporal Operated Token Program

### VC/DC
Victor Casado and David Chen
       
### Project Description:
A TOTP client/server implementation (both written in Python), with a custom HMAC function (written in C, using OpenSSL for hashing and `ctypes` FFI for Python linkage).

### Dependencies
- OpenSSL (`libssl`), development headers (`libssl-dev`) are needed to build the HMAC function.
- ZBar (`libzbar0`) is needed for the (optional) client QR decode feature.

### Instructions:
- `make client ARGS="otpauth://<...>`
  - Runs the TOTP generator program with the specified OTPAuth URI (following the Google Authenticator standard). Produces a token for the present time interval, and generates on loop successive tokens as the time increments upward.
  - Interaction is limited to `^C` to exit, and the single URI that can be inputted via command-line argument values.

- `make server`
  - Runs the Flask server program with a website that requests and verifies a TOTP with preset keys to verify that the user has access to said keys without explicitly transmitting the key (or a direct hash of it) via the network. (Note that Flask must be installed in the given environment.)
  - Interaction is via the web browser (default http://127.0.0.1:5001). User can enter an attempted TOTP, upon which they are informed as to whether they passed authentication or failed.

### Resources/ References:
- TOTP: Time-Based One-Time Password Algorithm ([RFC 6238](https://datatracker.ietf.org/doc/html/rfc6238))
  - HOTP: An HMAC-Based One-Time Password Algorithm ([RFC 4226](https://www.rfc-editor.org/rfc/rfc4226))
    - HMAC: Keyed-Hashing for Message Authentication ([RFC 2104](https://www.rfc-editor.org/rfc/rfc2104))
    - Secure Hash Standard (SHS) ([NIST FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final))
- Google Authenticator Key URI Format ([Google Authenticator GitHub Wiki](https://github.com/google/google-authenticator/wiki/Key-Uri-Format))

#### C Libraries
- [OpenSSL `SHA1()` function](https://docs.openssl.org/master/man3/SHA256_Init/)

#### Python Libraries
- [`base64` (with base32 support)](https://docs.python.org/3/library/base64.html)
- [`ctypes` (foreign-function interfaces)](https://docs.python.org/3/library/ctypes.html)
- [`urllib.parse` (for URI parsing)](https://docs.python.org/3/library/urllib.parse.html)
- [`pyzbar` (optional, for QR decode)](https://pypi.org/project/pyzbar/)
