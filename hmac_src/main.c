#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>

// SHA-1 related byte-count constants, see RFC 2104 for definitions
#define B 64
#define L 20

int main(int argc, char* argv[]) {
	if (argc < 3) {
		fprintf(stderr, "Usage: %s infile hexkey\n", argv[0]);
		return 1;
	}
	size_t K_len = (strlen(argv[2]) + 1) / 2;  // 2 hex digits to a byte, rounding up
	unsigned char* K = malloc(K_len * (sizeof(char)));
	unsigned char* buf;
	buf = SHA1(argv[2], strlen(argv[2]), NULL);
	for (int i = 0; i < 20; i++) {
		printf("%02x", buf[i]);
	}
	// fopen(argv[1], "rb");

}
