# NOTE: you might want to adapt this to your Python version and OS.
# As of today Cygwin supports Python 3.9 and Ubuntu 22.04 is at 3.10.
CYGWIN := no
PYTHON := 3.10

ifeq ($(CYGWIN),yes)
INCLUDES  := -I/usr/include/python$(PYTHON)/
LIBRARIES := -L/bin/ -lpython$(PYTHON)
TARGET    := spam.dll
else
INCLUDES  := -I/usr/include/python$(PYTHON)/
LIBRARIES := -L/lib/x86_64-linux-gnu -lpython$(PYTHON)
TARGET    := spam.so
endif

CC        := gcc
CPPFLAGS  := $(INCLUDES)

all: src/spam.c
	$(CC) $(CPPFLAGS) -O3 -g -shared $(LIBRARIES) src/spam.c -o $(TARGET)

clean:
	rm -rf $(TARGET)
