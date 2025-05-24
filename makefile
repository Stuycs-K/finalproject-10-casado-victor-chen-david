.PHONY: client server clean

client: shared/hmac_sha1.so
	@python3 client/main.py "$(ARGS)"
server: shared/hmac_sha1.so
	@python3 server/__init__.py

shared/hmac_sha1.so: shared/hmac_sha1.c
	@cc -shared -fPIC -o shared/hmac_sha1.so shared/hmac_sha1.c -lcrypto
shared/hmac_sha1.test: shared/hmac_sha1.c
	@gcc -o shared/hmac_sha shared/hmac_sha1.c -lcrypto

clean:
	@rm -rf shared/hmac_sha1.so shared/hmac_sha1.test __pycache__/
