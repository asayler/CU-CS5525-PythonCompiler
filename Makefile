# File: Makefile
# By: Andy Sayler <www.andysayler.com>
# CU CS 5525 - Compilers
# Creation Date: 2012/09/06
# Modififed Date: 2012/09/06
# Description:
#	This is the Makefile for the compiler test files


CC = gcc
PC = ./compile.py
CP = cp

CFLAGS = -c -m32 -g
LFLAGS = -m32 -g

SUBMISSIONDIR = ../submit/
HELPERDIR = ./helper/

TESTCASESSOURCE = $(wildcard test/p0/*.py)
TESTCASESASSEMB = $(patsubst test/p0/%.py,%.s,$(TESTCASESSOURCE))
TESTCASES = $(patsubst %.s,%.out,$(TESTCASESASSEMB))

.PHONY: all clean submission

all: $(TESTCASES)

%.out: %.s runtime.o hashtable.o hashtable_itr.o hashtable_utility.o
	$(CC) $(LFLAGS) $^ -lm -o $@

%.s: test/p0/%.py
	$(PC) $^

runtime.o: helper/runtime.c helper/runtime.h
	$(CC) $(CFLAGS) $< -o $@

hashtable.o: helper/hashtable.c helper/hashtable.h
	$(CC) $(CFLAGS) $< -o $@

hashtable_itr.o: helper/hashtable_itr.c helper/hashtable_itr.h 
	$(CC) $(CFLAGS) $< -o $@

hashtable_utility.o: helper/hashtable_utility.c helper/hashtable_utility.h
	$(CC) $(CFLAGS) $< -o $@

submission:
	$(RM) -r $(SUBMISSIONDIR)
	mkdir $(SUBMISSIONDIR)
	$(CP) $(PC) $(SUBMISSIONDIR)
	$(CP) $(HELPERDIR)* $(SUBMISSIONDIR)
	zip -j submit.zip $(SUBMISSIONDIR)*
	$(RM) -r $(SUBMISSIONDIR)

clean:
	$(RM) $(TESTCASES)
	$(RM) *.o
	$(RM) *.out
	$(RM) *.s
	$(RM) *~
	$(RM) *.pyc
	$(RM) submit.zip
