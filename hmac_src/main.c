#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <errno.h>
#include <sys/stat.h>
#include <string.h>
#include <openssl/sha.h>

#define PANIC() fprintf(stderr, "%s\n", strerror(errno)); return errno;

// see RFC 2104 for definitions
// SHA-1 related byte-count constants
#define B 64
#define L 20
// RFC 2104 specific constant bytestrings
#define IPAD 0x36
#define OPAD 0x5C


unsigned char hex_to_nibble(unsigned char h) {
	int b = tolower(h);
	switch(b) {
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
			return (unsigned char)(b + 10 - 'a');
	}
	return -1;
}

int main(int argc, char* argv[]) {
	if (argc < 3) {
		fprintf(stderr, "Usage: %s infile hexkey\n", argv[0]);
		return 1;
	}
	size_t len = (strlen(argv[2]) + 1) / 2;  // 2 hex digits to a byte, rounding up
	unsigned char* K = malloc(len * (sizeof(char)));
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
	if (len > B) {
		buf = K;
		K = SHA1(K, len, malloc(L * sizeof(char)));
		len = L;
		free(buf);
	}
	if (len < B) {
		buf = K;
		K = calloc(B, sizeof(char));
		memcpy(K, buf, len);
		free(buf);
	}
	// see 2104.2.2-3
	struct stat stat_buf;
	if (stat(argv[1], &stat_buf)) {
		fprintf(stderr, "%s\n", strerror(errno));
		return errno;
	};

	len = B + stat_buf.st_size;
	unsigned char* K_ipad = malloc(sizeof(char) * len);
	for (int i = 0; i < B; i++)
		K_ipad[i] = K[i] ^ IPAD;

	FILE *in;
	if (!(in = fopen(argv[1], "rb"))) {
		PANIC()
	}
	if (fread(K_ipad+B, sizeof(char), stat_buf.st_size, in) != stat_buf.st_size) {
		PANIC()
	}

	// see 2104.2.4
	unsigned char* H_4 = SHA1(K_ipad, len, NULL);
#ifdef DEBUG
	for (int i = 0; i < L; i++) {
		printf("%02x", H_4[i]);
	}
#endif
	len = B + L;
	unsigned char* K_opad = malloc(len * sizeof(char));
	for (int i = 0; i < B; i++)
		K_opad[i] = K[i] ^ OPAD;
	memcpy(K_opad+B, H_4, L);
	unsigned char* ret = SHA1(K_opad, len, malloc(L));
	free(K);
	free(K_ipad);
	free(K_opad);
	for (int i = 0; i < L; i++)
		printf("%02x", ret[i]);
	printf("\n");
}
