# Dev Log:

This document must be updated daily every time you finish a work session.

## David Chen

### 2025-05-13 - RFC Reading
Read up on [RFC 6238](https://datatracker.ietf.org/doc/html/rfc6238) (TOTP) and [RFC 4226](https://datatracker.ietf.org/doc/html/rfc4226) (HOTP) which it is based on. Thought about how to split the team's work (will probably look into implementing the HMAC part myself so as to avoid this from being a trivial "follow the instructions/reference implementation" project - that part I'll leave for Victor).

### 2025-05-14 - AP Physics

Took and hopefully got a 5 on the AP Physics C examination
^ written by Victor in my stead (appreciated!), Mechanics today and E&M tomorrow...

### 2025-05-15 - AP Physics Again (not to be confused with AP Physics 2)
Will be out one more day for the E&M exam... asked Victor to take a look at the RFCs and think about what language he'll be using so we can integrate accordingly [might build my hashing part as a separate program to execute in lieu of good FFI], We Will See what happens... (this is being written during 2025-05-14)

Reviewed Victor's notes on what his understanding is of RFC 6238 and friends, thought about potential additional features we could add ("time travel" by iterating through a variety of possible T/C values).

### 2025-05-16 - Coordination and Cooperation
Hammered out the details of our proposal, how exactly we will be structuring this program (Python program [for easier Flasking later] that calls the HMACing program (originally `openssl mac -digest SHA1 -macopt hexkey:<secret> -in <datafile> HMAC`, to be replaced with my custom implementation of the HMAC + SHA program)).

### 2025-05-18 - Implementation Investigation
Read up on the definition of HMAC from [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104), along with the NIST definition of SHA-1 and friends in the [Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final).

Made a working example of using OpenSSL's [`SHA1()` function](https://docs.openssl.org/master/man3/SHA256_Init/) for our hashing needs. In theory we can reimplement SHA-1 if necessary (AKA for funsies), but for now we will constrain ourselves to just implementing HMAC (though for what it's worth, OpenSSL does have its own [HMAC facilities](https://docs.openssl.org/master/man3/HMAC/#description)).

### 2025-05-19
Discussed a potential bug in Victor's implementation (multiplying by -1 instead of masking the 32nd bit, which would definitely lead to funky business due to two's complement encoding and all), how we will test compatibility with other systems (safe to assume other TOTP services are using SHA1 ~~even though NIST has that deprecated with 2030 being the deadline~~, we can parse the QR code to get the secret and other metadata).

In class, Implemented reading of K from the command line arguments, along with hashing/padding to fit the B-byte structure of the key.

At home, implemented remaining steps of the HMAC standard, began checking for parity with the Python HMAC implementation Victor is using. While troubleshooting, noticed that hex string padding convention differs (Python 0-pads the leading byte, I 0-pad the terminating byte), leading to differing hashes.

### 2025-05-20
Fixed the 0-pad issue, HMAC-SHA1s now match! Talked to Victor about using foreign-function interfaces to integrate our codebases.

Rearranged code to build into a shared object for use with FFI.

At home: Learned enough `ctypes` to call the custom `hmac_sha1()` function from Python, though it is now definitely broken where it wasn't before...
