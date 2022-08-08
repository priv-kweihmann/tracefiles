// SPDX-FileCopyrightText: 2022 Konrad Weihmann
// SPDX-License-Identifier: BSD-2-Clause

#include <stdio.h>

#include "external.h"

void external_function(char* input) {
    if (input != NULL) {
        printf("Hello %s\n", input);
    }
}