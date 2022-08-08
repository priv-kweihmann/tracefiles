# SPDX-FileCopyrightText: 2022 Konrad Weihmann
# SPDX-License-Identifier: BSD-2-Clause

CC ?= gcc
CCFLAGS := -g
CCOBJFLAGS := $(CCFLAGS) -c
OBJCOPY ?= objcopy
STRIP ?= strip

# path macros
BIN_PATH := bin
OBJ_PATH := obj
SRC_PATH := src
DBG_PATH := $(BIN_PATH)/.debug
PKG_PATH := packages

# compile macros
TARGET_NAME := demoapp
TARGET := $(BIN_PATH)/$(TARGET_NAME)

# src files & obj files
SRC := $(foreach x, $(SRC_PATH), $(wildcard $(addprefix $(x)/*,.c*)))
OBJ := $(addprefix $(OBJ_PATH)/, $(addsuffix .o, $(notdir $(basename $(SRC)))))

# default rule
default: makedir all

# non-phony targets
$(TARGET): $(OBJ)
	$(CC) $(CCFLAGS) $(OBJ) -o $@
	$(OBJCOPY) --only-keep-debug $(BIN_PATH)/$(TARGET_NAME) $(DBG_PATH)/$(TARGET_NAME)
	$(STRIP) --strip-debug --strip-unneeded $(BIN_PATH)/$(TARGET_NAME)

packgage: $(TARGET)
	install -d $(PKG_PATH)/pkg1/usr/bin/
	install -d $(PKG_PATH)/pkg1/usr/share/sub/folder1/

	install -m 0755 $(TARGET) $(PKG_PATH)/pkg1/usr/bin/
	install -m 0644 $(SRC_PATH)/sub/folder1/plain $(PKG_PATH)/pkg1/usr/share/sub/folder1/
	install -m 0644 $(SRC_PATH)/template.in $(PKG_PATH)/pkg1/usr/share/template

	install -d $(PKG_PATH)/pkg1-dbg/usr/bin/.debug/
	install -m 0755 $(DBG_PATH)/$(TARGET_NAME) $(PKG_PATH)/pkg1-dbg/usr/bin/.debug/

$(OBJ_PATH)/%.o: $(SRC_PATH)/%.c*
	$(CC) $(CCOBJFLAGS) -o $@ $<

# phony rules
.PHONY: makedir
makedir:
	@mkdir -p $(BIN_PATH) $(OBJ_PATH) $(DBG_PATH) $(PKG_PATH)

.PHONY: all
all: $(TARGET) packgage

.PHONY: clean
clean:
	@rm -rf $(BIN_PATH) $(OBJ_PATH) $(DBG_PATH) $(PKG_PATH)