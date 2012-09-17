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
MV = mv

CFLAGS = -c -m32 -g
LFLAGS = -m32 -g

SUBMISSIONDIR = ../submit-compiler/
HELPERDIR = ./helper/
PLYDIR = ./ply/

P0TESTDIR = ./test/p0/
P0TESTCASESSOURCE = $(wildcard $(P0TESTDIR)*.py)
P0TESTCASESINPUT  = $(wildcard $(P0TESTDIR)*.in)
P0TESTCASESASSEMB = $(patsubst $(P0TESTDIR)%.py, %.s, $(P0TESTCASESSOURCE))
P0TESTCASES = $(patsubst %.s, %.out, $(P0TESTCASESASSEMB))

.PHONY: all clean submission P0Tests

all: P0Tests

P0Tests: $(P0TESTCASES)

%.out: %.s runtime.o hashtable.o hashtable_itr.o hashtable_utility.o
	$(CC) $(LFLAGS) $^ -lm -o $@

$(P0TESTCASESASSEMB): %.s: $(P0TESTDIR)%.py *.py
	$(PC) $<

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
	$(CP) *.py $(SUBMISSIONDIR)
	$(CP) $(HELPERDIR)* $(SUBMISSIONDIR)
	$(CP) -r $(PLYDIR) $(SUBMISSIONDIR)
	zip -j submit.zip $(SUBMISSIONDIR)*
	$(RM) -r $(SUBMISSIONDIR)

clean:
	$(RM) $(P0TESTCASES)
	$(RM) *.o
	$(RM) *.out
	$(RM) *.s
	$(RM) *~
	$(RM) *.pyc
	$(RM) submit.zip
	$(RM) parsetab.py
