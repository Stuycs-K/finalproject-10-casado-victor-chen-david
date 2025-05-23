.PHONY: all run

run: hmac_sha1.so
	@python3 main.py

all: hmac_sha1.so hmac_sha1.test

hmac_sha1.so: hmac_sha1.c
	@gcc -shared -o hmac_sha1.so -lcrypto -fPIC hmac_sha1.c
hmac_sha1.test: hmac_sha1.c
	@gcc -o hmac_sha hmac_sha1.c -lcrypto

clean:
	-rm -f hmac_sha1.so hmac_sha1.test
