#include <stdio.h>
#include "pico/stdlib.h"

const int TRUE = 1;

int main () {
	stdio_init_all();

	while (TRUE) {
		printf("Hello, world!\n");
		sleep_ms(1000);
	}
	return 0;
}
