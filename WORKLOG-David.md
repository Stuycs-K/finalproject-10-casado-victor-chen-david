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

### 2025-05-21
Compared HMAC code to old revision `93e1a49`, did not see the misimplementation...

Since Victor was not around in class, helped him set up the SO import in WSL (seems there's a need to actually use `LD_PRELOAD` because something in the environment wasn't getting the libraries right). Still no dice on finding the hidden bug...

### 2025-05-22
Tested against the MD5 examples in the RFC 2104 examples in the appendix (see `md5` branch). Turns out I flipped the arguments in the Python wrapper...

Begin using `urllib` to parse otpauth URIs exported from our TOTP apps.

At home: Implemented parsing of otpauth URIs based on the [Google Authenticator](https://github.com/google/google-authenticator/wiki/Key-Uri-Format) key URI format, modified main Python script's timings and inputs to accomodate these changes. Successfully generated 2FA codes in testing with a TETR.IO account that had 2FA enabled.

### 2025-05-23
Organized client-relevant code into an independent folder in preparation for implementation of the server (anticipating merge conflicts later but those are trivially easy); debugged failure to automatically link libcrypto on StuyCS machines, fixed makefile recipes.

Merged the `makefile` and `main` branches, fixed unquoted `&` characters when passing key URIs as arguments, reorganized code such that shared functions were deduplicated, and a central makefile was sufficient to interface with all features of the project. Filled out the README with details gathered throughout the creation process.

### 2025-05-27
Tested merged code with Victor, removed broken function overload in `shared.py`. Used `lynx` to access builds on Marge.
Established plans for `PRESENTATION.md`, explaining the details of all 3 core RFCs (2104, 4226, 6238), schedule for following days.
Wrote additional notes on the 3 RFCs for `PRESENTATION.md`.

### 2025-05-28
Talked with Victor about implementing QR code output on the server, input on the client for more efficient demonstrations; discussed PRESENTATION.md contents (and how it would correspond with the video). Will have to make a makefile rule for... installing virtual environments...

Implemented makefile-based venv management, added QR code reading on the client side.

### 2025-05-29
Polished venv contents to include QR encode for the server, added helpful message to the venv makefile rule so that users are not confused by the wait.
Documented library dependencies.
Worked with Victor on implementing QR code display on the server.

Reviewed plans for video presentation, practiced demonstration of client operations.

### 2025-05-30
Helped Victor with web UI polishing, deployment of the server to a DigitalOcean droplet running NGINX.
Made plans to practicen and record video next week.

### 2025-06-01
Tested hosted version of the server against both our custom client (using QR code decode functionality) and FreeOTP+ on my phone.

### 2025-06-02
Got caught using our phones :(
Testing using a standard TOTP app on mobile (FreeOTP+) only to realize that the app suppresses screenshots/screen recordings so that wouldn't work; downloaded a random TOTP app off of F-Droid that didn't have that feature for the sake of later demonstrations.
Polish heading hierarchy for PRESENTATION.md, push symlink in case of case sensitivity.

Planned out call recording setup for our video, OBS on my laptop and local screen recording on my phone.

Recorded first takes at the video, after much fighting my VFX software realized the final cut wasn't satisfactory; will probably see about revising the script tomorrow...

### 2025-06-03
Revised script, recorded video, trimmed out glitches from bad network connection and the like. Uploaded video to YouTube and added to README!
