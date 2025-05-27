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

February 1997 December 2005 May 2011
RFC 2104
HMAC

#### RFC 4226

#### HOTP

#### RFC 6238

#### TOTP


### HMAC

Message Authentication Codes


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


