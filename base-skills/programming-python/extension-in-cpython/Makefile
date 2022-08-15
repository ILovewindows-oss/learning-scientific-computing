CYGWIN := yes

ifeq ($(CYGWIN),yes)
INCLUDES  := -I/usr/include/python3.9/
LIBRARIES := -L/bin/ -lpython3.9
TARGET    := spam.dll
else
# INCLUDES  := -I/usr/include/python3.9/
# LIBRARIES := -L/bin/ -lpython3.9
# TARGET    := spam.so
endif

CC        := gcc
CPPFLAGS  := $(INCLUDES)

all: src/spam.c
	$(CC) $(CPPFLAGS) -O3 -g -shared $(LIBRARIES) src/spam.c -o $(TARGET)

clean:
	rm -rf $(TARGET)
