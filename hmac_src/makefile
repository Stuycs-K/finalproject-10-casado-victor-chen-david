.PHONY: all run
run: hmac_sha
	@./hmac_sha $(ARGS)

all: hmac_sha

hmac_sha: main.c
	@gcc -o hmac_sha main.c -lcrypto
hmac_sha.so: main.c
	@gcc -shared -o hmac_sha.so -lcrypto -fPIC main.c

clean:
	-rm -f hmac_sha hmac_sha.so
