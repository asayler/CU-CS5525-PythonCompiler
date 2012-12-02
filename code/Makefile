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
AS = gcc
PC = ./compile.py
CP = cp
MV = mv
CD = cd

CFLAGS  = -c -m32 -g
ASFLAGS = -g -x assembler
LFLAGS  = -m32 -g
PCFLAGS = #-v 0 --dot

LLAS      = clang
LLASFLAGS = -g -x assembler
LLI       = lli
LLIFLAGS  =
LLC       = llc
LLCFLAGS  =
LLA       = llvm-as
LLAFLAGS  =
LLL       = llvm-link
LLLFLAGS  = 
LLCC      = clang
LLCCFLAGS = -emit-llvm

SUBMISSIONDIR = ./submission/
HELPERDIR     = ./helper/
BUILDDIR      = ./build/
TESTDIR       = ./test/

HELPERSOURCE = $(wildcard $(HELPERDIR)*.c)
HELPEROBJECT = $(patsubst $(HELPERDIR)%.c, $(BUILDDIR)%.o,  $(HELPERSOURCE))
HELPERLLVMLL = $(patsubst $(HELPERDIR)%.c, $(BUILDDIR)%.ll, $(HELPERSOURCE))
HELPERLLVMBC = $(patsubst $(BUILDDIR)%.ll, $(BUILDDIR)%.bc, $(HELPERLLVMLL))

MTESTCASESLL  = $(wildcard $(TESTDIR)*.ll)
MTESTCASESBC  = $(patsubst $(TESTDIR)%.ll,    $(BUILDDIR)%.mbc,   $(MTESTCASESLL))
MTESTCASESLBC = $(patsubst $(BUILDDIR)%.mbc,  $(BUILDDIR)%.mlbc,  $(MTESTCASESBC))
MTESTCASESASS = $(patsubst $(BUILDDIR)%.mlbc, $(BUILDDIR)%.ms,    $(MTESTCASESLBC))
MTESTCASES    = $(patsubst $(BUILDDIR)%.ms,   $(BUILDDIR)%.mout,  $(MTESTCASESASS))

TESTCASESSOURCE   = $(wildcard $(TESTDIR)*.py)
TESTCASESINPUT    = $(patsubst %.py,               %.in,                $(TESTCASESSOURCE))
TESTCASESASS86    = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.s,      $(TESTCASESSOURCE))
TESTCASESOUT86    = $(patsubst $(BUILDDIR)%.s,     $(BUILDDIR)%.86out,  $(TESTCASESASS86))
TESTDIFFS86       = $(patsubst $(BUILDDIR)%.86out, $(BUILDDIR)%.86diff, $(TESTCASESOUT86))
TESTCASESLL       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.ll,     $(TESTCASESSOURCE))
TESTCASESBC       = $(patsubst $(BUILDDIR)%.ll,    $(BUILDDIR)%.bc,     $(TESTCASESLL))
TESTCASESLBC      = $(patsubst $(BUILDDIR)%.bc,    $(BUILDDIR)%.lbc,    $(TESTCASESBC))
TESTCASESASSLL    = $(patsubst $(BUILDDIR)%.lbc,   $(BUILDDIR)%.lls,    $(TESTCASESLBC))
TESTCASESOUTLL    = $(patsubst $(BUILDDIR)%.lls,   $(BUILDDIR)%.llout,  $(TESTCASESASSLL))
TESTDIFFSLL       = $(patsubst $(BUILDDIR)%.llout, $(BUILDDIR)%.lldiff, $(TESTCASESOUTLL))


.PHONY: all clean \
	Assemb Assemb86 AssembLL \
	Tests Tests86 TestsLL \
	TestsRun TestsRun86 TestsRunLL \
	MTests

all: Tests

MTests: $(MTESTCASES)

Assemb: Assemb86

AssembLL: $(TESTCASESASSLL)

Assemb86: $(TESTCASESASS86)

Tests: Tests86

Tests86: $(TESTCASESOUT86)

TestsLL: $(TESTCASESOUTLL)

TestsRun: TestsRun86

TestsRun86: $(TESTDIFFS86)
	cat $^

TestsRunLL: $(TESTDIFFSLL)
	cat $^

$(TESTDIFFS86): $(BUILDDIR)%.86diff: $(BUILDDIR)%.86out $(TESTDIR)%.in
	cat $(TESTDIR)$*.in | $(BUILDDIR)$*.86out > $(BUILDDIR)$*.86output
	cat $(TESTDIR)$*.in | $(TESTDIR)$*.py > $(BUILDDIR)$*.correct
	diff -B -s -q $(BUILDDIR)$*.86output $(BUILDDIR)$*.correct > $@

$(TESTDIFFSLL): $(BUILDDIR)%.lldiff: $(BUILDDIR)%.llout $(TESTDIR)%.in
	cat $(TESTDIR)$*.in | $(BUILDDIR)$*.llout > $(BUILDDIR)$*.lloutput
	cat $(TESTDIR)$*.in | $(TESTDIR)$*.py > $(BUILDDIR)$*.correct
	diff -B -s -q $(BUILDDIR)$*.lloutput $(BUILDDIR)$*.correct > $@

$(TESTCASESOUT86): $(BUILDDIR)%.86out: $(BUILDDIR)%.s $(HELPEROBJECT)
	$(CC) $(LFLAGS) $^ -lm -o $@

$(TESTCASESASS86): $(BUILDDIR)%.s: $(TESTDIR)%.py *.py
	$(PC) $(PCFLAGS) $< -o $@

$(TESTCASESOUTLL): $(BUILDDIR)%.llout: $(BUILDDIR)%.lls
	$(LLAS) $(LLASFLAGS) $< -lm -o $@

$(TESTCASESASSLL): $(BUILDDIR)%.lls: $(BUILDDIR)%.lbc
	$(LLC) $(LLCFLAGS) $< -o $@

$(TESTCASESLBC): $(BUILDDIR)%.lbc: $(BUILDDIR)%.bc $(HELPERLLVMBC)
	$(LLL) $(LLLFLAGS) $^ -o $@

$(TESTCASESBC): $(BUILDDIR)%.bc: $(BUILDDIR)%.ll
	$(LLA) $(LLAFLAGS) $< -o $@

$(TESTCASESLL): $(BUILDDIR)%.ll: $(TESTDIR)%.py *.py
	$(PC) $(PCFLAGS) $< -o $@

$(MTESTCASES): $(BUILDDIR)%.mout: $(BUILDDIR)%.ms
	$(LLAS) $(LLASFLAGS) $< -lm -o $@

$(MTESTCASESASS): $(BUILDDIR)%.ms: $(BUILDDIR)%.mlbc
	$(LLC) $(LLCFLAGS) $< -o $@

$(MTESTCASESLBC): $(BUILDDIR)%.mlbc: $(BUILDDIR)%.mbc $(HELPERLLVMBC)
	$(LLL) $(LLLFLAGS) $^ -o $@

$(MTESTCASESBC): $(BUILDDIR)%.mbc: $(TESTDIR)%.ll
	$(LLA) $(LLAFLAGS) $< -o $@

$(HELPEROBJECT): $(BUILDDIR)%.o: $(HELPERDIR)%.c $(HELPERDIR)*.h
	$(CC) $(CFLAGS) $< -o $@

$(HELPERLLVMBC): $(BUILDDIR)%.bc: $(BUILDDIR)%.ll
	$(LLA) $(LLAFLAGS) $< -o $@

$(HELPERLLVMLL): $(BUILDDIR)%.ll: $(HELPERDIR)%.c $(HELPERDIR)*.h
	$(LLCC) $(LLCCFLAGS) -S $< -o $@

submission:
	$(RM) -r $(SUBMISSIONDIR)
	mkdir $(SUBMISSIONDIR)
	$(CP) *.py $(SUBMISSIONDIR)
	$(CP) $(HELPERDIR)*.c $(SUBMISSIONDIR)
	$(CP) $(HELPERDIR)*.h $(SUBMISSIONDIR)
	$(CD) $(SUBMISSIONDIR); zip -r ../submit.zip *
	$(RM) -r $(SUBMISSIONDIR)

clean:
	$(RM) $(TESTCASES)
	$(RM) *~
	$(RM) $(BUILDDIR)*
	$(RM) $(TESTDIR)*~
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
