# File: Makefile
#
# By: Andy Sayler <www.andysayler.com>
# In association with:
#   Michael (Mike) Vitousek
#     https://github.com/mvitousek/python-compiler-mmv
#   Anne Gatchell
#     https://github.com/halloannielala/compiler-5525
#
# CU CS 5525 - Compilers
# Creation Date: 2012/09/06
#
# Description:
#     This is the Makefile for the compiler test files

CC = gcc
PC = ./compile.py
CP = cp
MV = mv
CD = cd

CFLAGS  = -c -m32 -g
LFLAGS  = -m32 -g
PCFLAGS = #-v 0 --dot

LLI       = lli
LLIFLAGS  =
LLC       = llc
LLCFLAGS  =
LLA       = llvm-as
LLAFLAGS  =
LLL       = llvm-link
LLLFLAGS  = 
LLCC      = clang
LLCCFLAGS = 
LLCA      = clang
LLCAFLAGS = -emit-llvm

SUBMISSIONDIR = ./submission/
HELPERDIR = ./helper/
BUILDDIR = ./build/
TESTDIR = ./test/

HELPERSOURCE = $(wildcard $(HELPERDIR)*.c)
HELPEROBJECT = $(patsubst $(HELPERDIR)%.c, $(BUILDDIR)%.o,  $(HELPERSOURCE))
HELPERLLVMBC = $(patsubst $(HELPERDIR)%.c, $(BUILDDIR)%.bc, $(HELPERSOURCE))

TESTCASESSOURCE = $(wildcard $(TESTDIR)*.py)
TESTCASESINPUT  = $(patsubst %.py,           %.in,           $(TESTCASESSOURCE))
TESTCASESASSEMB = $(patsubst $(TESTDIR)%.py, $(BUILDDIR)%.s, $(TESTCASESSOURCE))
TESTCASES       = $(patsubst $(BUILDDIR)%.s, $(BUILDDIR)%.out,  $(TESTCASESASSEMB))
TESTDIFFS       = $(patsubst $(BUILDDIR)%.out, $(BUILDDIR)%.diff, $(TESTCASES))

.PHONY: all clean Tests TestsRun llvmbc

all: Tests

llvmbc: $(HELPERLLVMBC)

Assemb: $(TESTCASESASSEMB)

Tests: $(TESTCASES)

TestsRun: $(TESTDIFFS)
	cat $^

$(TESTDIFFS): $(BUILDDIR)%.diff: $(BUILDDIR)%.out $(TESTDIR)%.in
	cat $(TESTDIR)$*.in | $(BUILDDIR)$*.out > $(BUILDDIR)$*.output
	cat $(TESTDIR)$*.in | $(TESTDIR)$*.py > $(BUILDDIR)$*.correct
	diff -B -s -q $(BUILDDIR)$*.output $(BUILDDIR)$*.correct > $@

$(TESTCASES): $(BUILDDIR)%.out: $(BUILDDIR)%.s $(HELPEROBJECT)
	$(CC) $(LFLAGS) $^ -lm -o $@

$(TESTCASESASSEMB): $(BUILDDIR)%.s: $(TESTDIR)%.py *.py
	$(PC) $(PCFLAGS) $<
	$(MV) $(@F) $(BUILDDIR)

$(HELPEROBJECT): $(BUILDDIR)%.o: $(HELPERDIR)%.c $(HELPERDIR)*.h
	$(CC) $(CFLAGS) $< -o $@

$(HELPERLLVMBC): $(BUILDDIR)%.bc: $(HELPERDIR)%.c $(HELPERDIR)*.h
	$(LLCA) $(LLCAFLAGS) -S $< -o $@

submission:
	$(RM) -r $(SUBMISSIONDIR)
	mkdir $(SUBMISSIONDIR)
	$(CP) *.py $(SUBMISSIONDIR)
	$(CP) $(HELPERDIR)* $(SUBMISSIONDIR)
	$(CD) $(SUBMISSIONDIR); zip -r ../submit.zip *
	$(RM) -r $(SUBMISSIONDIR)

clean:
	$(RM) $(TESTCASES)
	$(RM) $(BUILDDIR)*.o
	$(RM) $(BUILDDIR)*.out
	$(RM) $(BUILDDIR)*.s
	$(RM) $(BUILDDIR)*.output
	$(RM) $(BUILDDIR)*.correct
	$(RM) $(BUILDDIR)*.diff
	$(RM) *~
	$(RM) $(TESTDIR)*~
	$(RM) $(BUILDDIR)*~
	$(RM) $(HELPERDIR)*~
	$(RM) \#*\#
	$(RM) *.s
	$(RM) *.pyc
	$(RM) *.out
	$(RM) *.dot
	$(RM) *.svg
	$(RM) *.jpg
	$(RM) submit.zip
	$(RM) -r $(SUBMISSIONDIR)
