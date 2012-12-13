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

TIME 	  = /usr/bin/time

CC        = gcc
AS        = gcc
PC        = ./compile.py
CP        = cp
MV        = mv
CD        = cd

CFLAGS    = -c -m32 -g
ASFLAGS   = -g -x assembler
LFLAGS    = -m32 -g
PCFLAGS   = #-v 0 --dot

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

HELPERSOURCE        = $(wildcard $(HELPERDIR)*.c)
HELPEROBJECT        = $(patsubst $(HELPERDIR)%.c, $(BUILDDIR)%.o,  $(HELPERSOURCE))
HELPERLLVMLL        = $(patsubst $(HELPERDIR)%.c, $(BUILDDIR)%.ll, $(HELPERSOURCE))
HELPERLLVMBC        = $(patsubst $(BUILDDIR)%.ll, $(BUILDDIR)%.bc, $(HELPERLLVMLL))

MTESTCASESLL        = $(wildcard $(TESTDIR)*.ll)
MTESTCASESBC        = $(patsubst $(TESTDIR)%.ll,    $(BUILDDIR)%.mbc,   $(MTESTCASESLL))
MTESTCASESLBC       = $(patsubst $(BUILDDIR)%.mbc,  $(BUILDDIR)%.mlbc,  $(MTESTCASESBC))
MTESTCASESASS       = $(patsubst $(BUILDDIR)%.mlbc, $(BUILDDIR)%.ms,    $(MTESTCASESLBC))
MTESTCASES          = $(patsubst $(BUILDDIR)%.ms,   $(BUILDDIR)%.mout,  $(MTESTCASESASS))

TESTCASESSOURCE     = $(wildcard $(TESTDIR)*.py)

TESTCASESINPUT      = $(patsubst %.py,               %.in,                $(TESTCASESSOURCE))
TESTCASESASS86      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.s,      $(TESTCASESSOURCE))
TESTCASESOUT86      = $(patsubst $(BUILDDIR)%.s,     $(BUILDDIR)%.86out,  $(TESTCASESASS86))
TESTDIFFS86         = $(patsubst $(BUILDDIR)%.86out, $(BUILDDIR)%.86diff, $(TESTCASESOUT86))

TESTCASESLL         = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.ll,     $(TESTCASESSOURCE))
TESTCASESBC         = $(patsubst $(BUILDDIR)%.ll,    $(BUILDDIR)%.bc,     $(TESTCASESLL))
TESTCASESLBC        = $(patsubst $(BUILDDIR)%.bc,    $(BUILDDIR)%.lbc,    $(TESTCASESBC))
TESTCASESASSLL      = $(patsubst $(BUILDDIR)%.lbc,   $(BUILDDIR)%.lls,    $(TESTCASESLBC))
TESTCASESOUTLL      = $(patsubst $(BUILDDIR)%.lls,   $(BUILDDIR)%.llout,  $(TESTCASESASSLL))
TESTDIFFSLL         = $(patsubst $(BUILDDIR)%.llout, $(BUILDDIR)%.lldiff, $(TESTCASESOUTLL))

BMTESTCASESSOURCE   = $(wildcard $(TESTDIR)*benchmark*.py)
BMTESTDIFFS86       = $(patsubst $(TESTDIR)%.py,      $(BUILDDIR)%.86diff, $(BMTESTCASESSOURCE))
BMTESTDIFFSLL       = $(patsubst $(TESTDIR)%.py,      $(BUILDDIR)%.lldiff, $(BMTESTCASESSOURCE))
BMTESTRTLL          = $(patsubst $(BUILDDIR)%.lldiff, $(BUILDDIR)%.llrt,   $(BMTESTDIFFSLL))
BMTESTRT86          = $(patsubst $(BUILDDIR)%.86diff, $(BUILDDIR)%.86rt,   $(BMTESTDIFFS86))

LLVMTESTCASESSOURCE = $(wildcard $(TESTDIR)*llvm*.py)
LLVMTESTDIFFS86     = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff, $(LLVMTESTCASESSOURCE))
LLVMTESTDIFFSLL     = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.lldiff, $(LLVMTESTCASESSOURCE))

P0TESTCASESSOURCE   = $(wildcard $(TESTDIR)test-p0-*.py)
P0TESTDIFFS86       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff, $(P0TESTCASESSOURCE))
P0TESTDIFFSLL       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.lldiff, $(P0TESTCASESSOURCE))

P1TESTCASESSOURCE   = $(wildcard $(TESTDIR)test-p1-*.py)
P1TESTDIFFS86       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff, $(P1TESTCASESSOURCE))
P1TESTDIFFSLL       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.lldiff, $(P1TESTCASESSOURCE))

P2TESTCASESSOURCE   = $(wildcard $(TESTDIR)test-p2-*.py)
P2TESTDIFFS86       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff, $(P2TESTCASESSOURCE))
P2TESTDIFFSLL       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.lldiff, $(P2TESTCASESSOURCE))

P3TESTCASESSOURCE   = $(wildcard $(TESTDIR)test-p3-*.py)
P3TESTDIFFS86       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff, $(P3TESTCASESSOURCE))
P3TESTDIFFSLL       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.lldiff, $(P3TESTCASESSOURCE))

PXTESTCASESSOURCE   = $(wildcard $(TESTDIR)test-pX-*.py)
PXTESTDIFFS86       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff, $(PXTESTCASESSOURCE))
PXTESTDIFFSLL       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.lldiff, $(PXTESTCASESSOURCE))

.PHONY: all clean \
	Assemb Assemb86 AssembLL \
	Tests Tests86 TestsLL \
	TestsRun TestsRun86 TestsRunLL \
	LLVMTestsRun86 LLVMTestsRunLL \
	P0TestsRun86 P0TestsRunLL \
	P1TestsRun86 P1TestsRunLL \
	P2TestsRun86 P2TestsRunLL \
	P3TestsRun86 P3TestsRunLL \
	PXTestsRun86 PXTestsRunLL \
	MTests BenchmarkTestsRun \
	BenchmarkTestsRunLL \
	BenchmarkTestsRun86

all: Tests

MTests: $(MTESTCASES)

Assemb: Assemb86

Assemb86: $(TESTCASESASS86)

AssembLL: $(TESTCASESASSLL)

Tests: Tests86 TestsLL

Tests86: $(TESTCASESOUT86)

TestsLL: $(TESTCASESOUTLL)

TestsRun: TestsRun86 TestsRunLL

TestsRun86: $(TESTDIFFS86)
	cat $^

TestsRunLL: $(TESTDIFFSLL)
	cat $^

BenchmarkTestsRun: BenchmarkTestsRunLL BenchmarkTestsRun86
	python analyze.py

BenchmarkTestsRunLL: $(BMTESTRTLL)

BenchmarkTestsRun86: $(BMTESTRT86)

LLVMTestsRun86: $(LLVMTESTDIFFS86)
	cat $^

LLVMTestsRunLL: $(LLVMTESTDIFFSLL)
	cat $^

P0TestsRun86: $(P0TESTDIFFS86)
	cat $^

P0TestsRunLL: $(P0TESTDIFFSLL)
	cat $^

P1TestsRun86: $(P1TESTDIFFS86)
	cat $^

P1TestsRunLL: $(P1TESTDIFFSLL)
	cat $^

P2TestsRun86: $(P2TESTDIFFS86)
	cat $^

P2TestsRunLL: $(P2TESTDIFFSLL)
	cat $^

P3TestsRun86: $(P3TESTDIFFS86)
	cat $^

P3TestsRunLL: $(P3TESTDIFFSLL)
	cat $^

PXTestsRun86: $(PXTESTDIFFS86)
	cat $^

PXTestsRunLL: $(PXTESTDIFFSLL)
	cat $^

$(TESTDIFFS86): $(BUILDDIR)%.86diff: $(BUILDDIR)%.86out $(TESTDIR)%.in
	cat $(TESTDIR)$*.in | $(BUILDDIR)$*.86out > $(BUILDDIR)$*.86output
	cat $(TESTDIR)$*.in | $(TESTDIR)$*.py > $(BUILDDIR)$*.correct
	diff -B -s -q $(BUILDDIR)$*.86output $(BUILDDIR)$*.correct > $@

$(BMTESTRT86): $(BUILDDIR)%.86rt: $(BUILDDIR)%.86out $(TESTDIR)%.in
	awk '{a+=$$0}END{print a}' $(BUILDDIR)$*.86ct > $(BUILDDIR)$*.86ctk
	mv $(BUILDDIR)$*.86ctk $(BUILDDIR)$*.86ct
	cat $(TESTDIR)$*.in | $(TIME) --format=%e -o $@ $(BUILDDIR)$*.86out

$(TESTDIFFSLL): $(BUILDDIR)%.lldiff: $(BUILDDIR)%.llout $(TESTDIR)%.in
	cat $(TESTDIR)$*.in | $(BUILDDIR)$*.llout > $(BUILDDIR)$*.lloutput
	cat $(TESTDIR)$*.in | $(TESTDIR)$*.py > $(BUILDDIR)$*.correct
	diff -B -s -q $(BUILDDIR)$*.lloutput $(BUILDDIR)$*.correct > $@

$(BMTESTRTLL): $(BUILDDIR)%.llrt: $(BUILDDIR)%.llout $(TESTDIR)%.in
	awk '{a+=$$0}END{print a}' $(BUILDDIR)$*.llct > $(BUILDDIR)$*.llctk
	mv $(BUILDDIR)$*.llctk $(BUILDDIR)$*.llct
	cat $(TESTDIR)$*.in | $(TIME) --format=%e -o $@ $(BUILDDIR)$*.llout

$(TESTCASESOUT86): $(BUILDDIR)%.86out: $(BUILDDIR)%.s $(HELPEROBJECT)
	$(TIME) --format=%e -o $(BUILDDIR)$*.86ct -a $(CC) $(LFLAGS) $^ -lm -o $@

$(TESTCASESASS86): $(BUILDDIR)%.s: $(TESTDIR)%.py *.py
	$(TIME) --format=%e -o $(BUILDDIR)$*.86ct $(PC) $(PCFLAGS) $< -o $@

$(TESTCASESOUTLL): $(BUILDDIR)%.llout: $(BUILDDIR)%.lls
	$(TIME) --format=%e -o $(BUILDDIR)$*.llct -a $(LLAS) $(LLASFLAGS) $< -lm -o $@

$(TESTCASESASSLL): $(BUILDDIR)%.lls: $(BUILDDIR)%.lbc
	$(TIME) --format=%e -o $(BUILDDIR)$*.llct -a $(LLC) $(LLCFLAGS) $< -o $@

$(TESTCASESLBC): $(BUILDDIR)%.lbc: $(BUILDDIR)%.bc $(HELPERLLVMBC)
	$(TIME) --format=%e -o $(BUILDDIR)$*.llct -a $(LLL) $(LLLFLAGS) $^ -o $@

$(TESTCASESBC): $(BUILDDIR)%.bc: $(BUILDDIR)%.ll
	$(TIME) --format=%e -o $(BUILDDIR)$*.llct -a $(LLA) $(LLAFLAGS) $< -o $@

$(TESTCASESLL): $(BUILDDIR)%.ll: $(TESTDIR)%.py *.py
	$(TIME) --format=%e -o $(BUILDDIR)$*.llct $(PC) $(PCFLAGS) $< -o $@

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
