### What is RFC tho? Who makes it? why

RFCs (Requests for Comments)
- Generally published by the Internet Engineering Task Force (IETF)
- Define standards, protocols, procedures, and best practices (including TCP/IP,
HTTP, DNS)
- Each RFC is individually numbered and once published, never changes (updates
are made with new RFCs)
- Widely used by developers, engineers, and researchers to ensure interoperability
and consistent implementation
- Serve as the foundation for internet architecture and communication protocols


### How did we get to RFC 6238?


|RFC|Title|Date|
|-|-|-|
|RFC 2104|HMAC: Keyed-Hashing for Message Authentication|February 1997|
|RFC 4226|HOTP: An HMAC-Based One-Time Password Algorithm|December 2005|
|RFC 6238|TOTP: Time-Based One-Time Password Algorithm|May 2011|

### HMAC
A Message Authentication Code (MAC) in general is an additional piece of data attached to a message to verify that the sender of the message holds the same secret key that the recipient does. The secret key should be shared between the two parties through another secure channel (e.g. HTTPS). It is important that it is **not** trivial to re-derive the secret key given an authenticated message (which may be transmitted over insecure channels, along with its MAC).

HMAC is a hash-based MAC (any secure hash algorithm can be used, we use SHA-1 for demonstration, but MD5 was used historically, and it is recommended to use SHA-2 hashes nowadays [but people default to SHA-1 despite its weaknesses and deprecation...]:).

HMAC is defined as taking in two byte sequences, a key string and a message string (i.e. byte arrays, can be non-ASCII):
1. Hashing an oversized key (if bigger than the block size of the hash) and padding the key with 0's to a minimum size (the hash block size `B`[^1]).
2. XORing said key with a specific byte pattern (`0x36 = 0011 0101` repeated) and appending the message contents.
3. Hashing all the data, then pre-pending the key XORed with a different pattern (`0x5c = 0101 1100`) and doing a second hash on the entire string of data.
This makes brute-forcing the key given the plaintext somewhat more difficult, as two layers of hashing operations are necessary.

Truncating an HMAC hash can be convenient (for reducing the odds of exposing the secret key/easier transmission), but can leave the authentication more vulnerable to birthday attacks (where it is easier for an attacker to simply stumble upon a hash that works because the latter bits happen to match).

[^1]: The keys are specified to fit the hash's block size so that intermediate values for the hashes can be pre-computed.

### HOTP
An HMAC-based One-Time Password uses HMAC (usually truncated for convenience) to generate one-time passwords, designed as a standard by the Open Authentication (OAuth) initiative in order to create standardized 2FA systems.

We achieve the one-time part of an OTP by using a numerical counter (synced between client and server) as the message string. After an HTOP is used once, it cannot be used again because the counter for both client and server will increment their counter. The key and counter should remain identical on both sides of the communication, and neither piece of data should be transmitted across insecure channels, giving an attacker very little information to work with, thus making brute force the primary option for "breaking" HOTP.

### TOTP
A TOTP is an HOTP, but instead of needing to keep a counter variable in sync, the counter is simply how many time increments (usually of 30 seconds) has passed since a certain time (usually the Unix Epoch, fixed at 1970-01-01 00:00 UTC).

## Steps to establishing TOTP

1. Information Sharing
    - Secret Key
    - Time interval
    - Hashing function
    - Code length
3. Code Generation
    - Unix Time
    - Secret Key
4. Code Verification
    - Multiple codes for ‘grace period’


# Security flaws

- Synchronization Errors
- Secret Key Exposure
- Phishing Attacks
- Code Reusability


