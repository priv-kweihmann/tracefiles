#include <stdio.h>

#include "external.h"

void external_function(char* input) {
    if (input != NULL) {
        printf("Hello %s\n", input);
    }
}