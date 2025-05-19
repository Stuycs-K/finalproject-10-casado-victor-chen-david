#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <errno.h>
#include <string.h>
#include <openssl/sha.h>

// SHA-1 related byte-count constants, see RFC 2104 for definitions
#define B 64
#define L 20

unsigned char hex_to_nibble(unsigned char h) {
	int b = tolower(h);
	switch(h) {
		case '\0':
			return 0;
		case '0':
		case '1':
		case '2':
		case '3':
		case '4':
		case '5':
		case '6':
		case '7':
		case '8':
		case '9':
			return (unsigned char)(b - '0');
		case 'a':
		case 'b':
		case 'c':
		case 'd':
		case 'e':
		case 'f':
			return (unsigned char)(b - 'a' + 10);
	}
	return -1;
}

int main(int argc, char* argv[]) {
	if (argc < 3) {
		fprintf(stderr, "Usage: %s infile hexkey\n", argv[0]);
		return 1;
	}
	size_t K_len = (strlen(argv[2]) + 1) / 2;  // 2 hex digits to a byte, rounding up
	unsigned char* K = malloc(K_len * (sizeof(char)));
	unsigned char* buf;
#ifdef DEBUG
	buf = SHA1(argv[2], strlen(argv[2]), NULL);
	for (int i = 0; i < 20; i++) {
		printf("%02x", buf[i]);
	}
#endif
	for (int i = 0; i < strlen(argv[2]); i+=2) {
		unsigned char buf;
		for (int j = 0; j < 2; j++) {
			buf = hex_to_nibble(argv[2][i+j]);
			if (buf & 11110000) {
				fprintf(stderr, "Invalid hex input `%c`\n", argv[2][i+j]);
				return 1;
			}
			if (j)
				K[i / 2] = K[i/2] << 4 | buf;
			else
				K[i / 2] = buf;
		}
	}
	if (K_len > B) {
		buf = K;
		K = SHA1(K, K_len, malloc(L * sizeof(char)));
		K_len = L;
		free(buf);
	}
	if (K_len < B) {
		buf = K;
		K = calloc(B, sizeof(char));
		memcpy(K, buf, K_len);
	}
	for (int i = 0; i < B; i++)
		printf("%02x ", K[i]);

	FILE *in;
	if (!(in = fopen(argv[1], "rb"))) {
		fprintf(stderr, "%s\n", strerror(errno));
		return errno;
	}

}
