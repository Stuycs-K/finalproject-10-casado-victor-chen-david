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

unsigned char* hmac_sha1(const unsigned char* K, size_t n, const unsigned char* text, size_t m);

#define DEBUG
int main(int argc, char* argv[]) {
	if (argc < 3) {
		fprintf(stderr, "Usage: %s infile hexkey\n", argv[0]);
		return 1;
	}
	size_t len = (strlen(argv[2]) + 1) / 2;  // 2 hex digits to a byte, rounding up
	unsigned char* K = malloc(len * (sizeof(char)));
	unsigned char* buf;
	for (int i = strlen(argv[2]) - 1; i >= 0; i-=2) {
		unsigned char buf;
		for (int j = 0; j < 2; j++) {
			buf = hex_to_nibble(argv[2][i-j]);
			if (buf & 11110000) {
				fprintf(stderr, "Invalid hex input `%c`\n", argv[2][i+j]);
				return 1;
			}
			if (j)
				K[i/2] = buf << 4 | K[i/2];
			else
				K[i/2] = buf;
		}
	}
#ifdef DEBUG
	for (int i = 0; i < len; i++) {
		printf("%02x", K[i]);
	}
	printf(" key\n");
#endif
	struct stat stat_buf;
	if (stat(argv[1], &stat_buf)) {
		fprintf(stderr, "%s\n", strerror(errno));
		return errno;
	};

	FILE *in;
	if (!(in = fopen(argv[1], "rb"))) {
		PANIC()
	}
	unsigned char *text = malloc(sizeof(char) * stat_buf.st_size);
	if (fread(text, sizeof(char), stat_buf.st_size, in) != stat_buf.st_size) {
		PANIC()
	}
	unsigned char* ret = hmac_sha1(K, len, text, stat_buf.st_size);
	for (int i = 0; i < L; i++)
		printf("%02x", ret[i]);
	printf("\n");

}
unsigned char* hmac_sha1(const unsigned char* K, size_t n, const unsigned char* text, size_t m) {
	unsigned char* key = memcpy(malloc(n * sizeof(char)), K, n);
#ifdef DEBUG
	printf("from C K: ");
	for (int i = 0; i < n; i++)
		printf("%02x", K[i]);
	printf("\n");
#endif
	if (n > B) {
		free(key);
		key = SHA1(K, n, malloc(L * sizeof(char)));
		n = L;
	}
	if (n < B) {
		unsigned char* tmp = calloc(B, sizeof(char));
		memcpy(tmp, key, n);
		free(key);
		key = tmp;
	}

	size_t inner_len = B + m;
	unsigned char* K_ipad = malloc(sizeof(char) * inner_len);
	for (int i = 0; i < B; i++)
		K_ipad[i] = key[i] ^ IPAD;
	memcpy(K_ipad+B, text, m);
#ifdef DEBUG
	printf("from C key: ");
	for (int i = 0; i < n; i++)
		printf("%02x", key[i]);
	printf("\n");
	printf("from C text: ");
	for (int i = 0; i < m; i++)
		printf("%02x", text[i]);
	printf("\nfrom C k_ipad: ");
	for (int i = 0; i < inner_len; i++)
		printf("%02x", K_ipad[i]);
	printf("\n");
#endif
	// see 2104.2.4
	unsigned char* H_4 = SHA1(K_ipad, inner_len, NULL);

	size_t outer_len = B + L;
	unsigned char* K_opad = malloc(outer_len * sizeof(char));
	for (int i = 0; i < B; i++)
		K_opad[i] = key[i] ^ OPAD;
	memcpy(K_opad+B, H_4, L);
	unsigned char* ret = SHA1(K_opad, outer_len, malloc(L));
	free(key);
	free(K_ipad);
	free(K_opad);
#ifdef DEBUG
	printf("from C: ");
	for (int i = 0; i < L; i++)
		printf("%02x", ret[i]);
	printf("\n");
#endif
	return ret;
}
