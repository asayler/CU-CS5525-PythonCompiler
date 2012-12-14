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
TIMEFLAGS = --format=%e

MAKE      = make

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
BENCHDIR      = ./bench/
TESTDIR       = ./test/
NULL          = /dev/null

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

TESTCASESLL         = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.ll,      $(TESTCASESSOURCE))
TESTCASESBC         = $(patsubst $(BUILDDIR)%.ll,    $(BUILDDIR)%.bc,      $(TESTCASESLL))
TESTCASESLBC        = $(patsubst $(BUILDDIR)%.bc,    $(BUILDDIR)%.lbc,     $(TESTCASESBC))
TESTCASESASSLL      = $(patsubst $(BUILDDIR)%.lbc,   $(BUILDDIR)%.lls,     $(TESTCASESLBC))
TESTCASESOUTLL      = $(patsubst $(BUILDDIR)%.lls,   $(BUILDDIR)%.llout,   $(TESTCASESASSLL))
TESTDIFFSLLC        = $(patsubst $(BUILDDIR)%.llout, $(BUILDDIR)%.llcdiff, $(TESTCASESOUTLL))
TESTDIFFSLLI        = $(patsubst $(BUILDDIR)%.lbc,   $(BUILDDIR)%.llidiff, $(TESTCASESLBC))

BMTESTCASESSOURCE   = $(wildcard $(TESTDIR)*benchmark*.py)
BMTESTDIFFS86       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff,  $(BMTESTCASESSOURCE))
BMTESTDIFFSLLC      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llcdiff, $(BMTESTCASESSOURCE))
BMTESTDIFFSLLI      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llidiff, $(BMTESTCASESSOURCE))
BMTESTCT86          = $(patsubst $(TESTDIR)%.py,     $(BENCHDIR)%.86ct,    $(BMTESTCASESSOURCE))
BMTESTRT86          = $(patsubst $(TESTDIR)%.py,     $(BENCHDIR)%.86rt,    $(BMTESTCASESSOURCE))
BMTESTCTLLC         = $(patsubst $(TESTDIR)%.py,     $(BENCHDIR)%.llcct,   $(BMTESTCASESSOURCE))
BMTESTRTLLC         = $(patsubst $(TESTDIR)%.py,     $(BENCHDIR)%.llcrt,   $(BMTESTCASESSOURCE))
BMTESTCTLLI         = $(patsubst $(TESTDIR)%.py,     $(BENCHDIR)%.llict,   $(BMTESTCASESSOURCE))
BMTESTRTLLI         = $(patsubst $(TESTDIR)%.py,     $(BENCHDIR)%.llirt,   $(BMTESTCASESSOURCE))

LLVMTESTCASESSOURCE = $(wildcard $(TESTDIR)*llvm*.py)
LLVMTESTDIFFS86     = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff,  $(LLVMTESTCASESSOURCE))
LLVMTESTDIFFSLLC    = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llcdiff, $(LLVMTESTCASESSOURCE))
LLVMTESTDIFFSLLI    = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llidiff, $(LLVMTESTCASESSOURCE))

PTESTCASESSOURCE    = $(wildcard $(TESTDIR)test-p?-*.py)
PTESTDIFFS86        = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff,  $(PTESTCASESSOURCE))
PTESTDIFFSLLC       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llcdiff, $(PTESTCASESSOURCE))
PTESTDIFFSLLI       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llidiff, $(PTESTCASESSOURCE))

P0TESTCASESSOURCE   = $(wildcard $(TESTDIR)test-p0-*.py)
P0TESTDIFFS86       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff,  $(P0TESTCASESSOURCE))
P0TESTDIFFSLLC      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llcdiff, $(P0TESTCASESSOURCE))
P0TESTDIFFSLLI      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llidiff, $(P0TESTCASESSOURCE))

P1TESTCASESSOURCE   = $(wildcard $(TESTDIR)test-p1-*.py)
P1TESTDIFFS86       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff,  $(P1TESTCASESSOURCE))
P1TESTDIFFSLLC      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llcdiff, $(P1TESTCASESSOURCE))
P1TESTDIFFSLLI      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llidiff, $(P1TESTCASESSOURCE))

P2TESTCASESSOURCE   = $(wildcard $(TESTDIR)test-p2-*.py)
P2TESTDIFFS86       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff,  $(P2TESTCASESSOURCE))
P2TESTDIFFSLLC      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llcdiff, $(P2TESTCASESSOURCE))
P2TESTDIFFSLLI      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llidiff, $(P2TESTCASESSOURCE))

P3TESTCASESSOURCE   = $(wildcard $(TESTDIR)test-p3-*.py)
P3TESTDIFFS86       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff,  $(P3TESTCASESSOURCE))
P3TESTDIFFSLLC      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llcdiff, $(P3TESTCASESSOURCE))
P3TESTDIFFSLLI      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llidiff, $(P3TESTCASESSOURCE))

PXTESTCASESSOURCE   = $(wildcard $(TESTDIR)test-pX-*.py)
PXTESTDIFFS86       = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.86diff,  $(PXTESTCASESSOURCE))
PXTESTDIFFSLLC      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llcdiff, $(PXTESTCASESSOURCE))
PXTESTDIFFSLLI      = $(patsubst $(TESTDIR)%.py,     $(BUILDDIR)%.llidiff, $(PXTESTCASESSOURCE))

.PHONY: all clean buildclean pycclean\
	Tests Tests86 TestsLLC TestsLLI \
	TestsRun TestsRun86 TestsRunLLC TestsRunLLI \
	LLVMTestsRun LLVMTestsRun86 LLVMTestsRunLLC LLVMTestsRunLLI \
	PTestsRun PTestsRun86 PTestsRunLLC PTestsRunLLI \
	P0TestsRun P0TestsRun86 P0TestsRunLLC P0TestsRunLLI \
	P1TestsRun P1TestsRun86 P1TestsRunLLC P1TestsRunLLI \
	P2TestsRun P2TestsRun86 P2TestsRunLLC P2TestsRunLLI \
	P3TestsRun P3TestsRun86 P3TestsRunLLC P3TestsRunLLI \
	PXTestsRun PXTestsRun86 PXTestsRunLLC PXTestsRunLLI \
	BenchmarkTestsRun BenchmarkTestsRun86 BenchmarkTestsRunLLC BenchmarkTestsRunLLI \
	MTests

all: Tests

MTests: $(MTESTCASES)

Tests: Tests86 TestsLLC TestsLLI

Tests86: $(TESTCASESOUT86)

TestsLLC: $(TESTCASESOUTLL)

TestsLLI: $(TESTCASESLBC)

TestsRun: TestsRun86 TestsRunLLC TestsRunLLI

TestsRun86: $(TESTDIFFS86)
	cat $^

TestsRunLLC: $(TESTDIFFSLLC)
	cat $^

TestsRunLLI: $(TESTDIFFSLLI)
	cat $^

BenchmarkTestsRun: BenchmarkTestsRun86 BenchmarkTestsRunLLI BenchmarkTestsRunLLC
	python analyze.py

BenchmarkTestsRun86: $(BMTESTRT86) $(BMTESTCT86)

BenchmarkTestsRunLLC: $(BMTESTRTLLC) $(BMTESTCTLLC)

BenchmarkTestsRunLLI: $(BMTESTRTLLI) $(BMTESTCTLLI)

LLVMTestsRun: LLVMTestsRun86 LLVMTestsRunLLC LLVMTestsRunLLI

LLVMTestsRun86: $(LLVMTESTDIFFS86)
	cat $^

LLVMTestsRunLLC: $(LLVMTESTDIFFSLLC)
	cat $^

LLVMTestsRunLLI: $(LLVMTESTDIFFSLLI)
	cat $^

PTestsRun: PTestsRun86 PTestsRunLLC PTestsRunLLI

PTestsRun86: $(PTESTDIFFS86)
	cat $^

PTestsRunLLC: $(PTESTDIFFSLLC)
	cat $^

PTestsRunLLI: $(PTESTDIFFSLLI)
	cat $^

P0TestsRun: P0TestsRun86 P0TestsRunLLC P0TestsRunLLI

P0TestsRun86: $(P0TESTDIFFS86)
	cat $^

P0TestsRunLLC: $(P0TESTDIFFSLLC)
	cat $^

P0TestsRunLLI: $(P0TESTDIFFSLLI)
	cat $^

P1TestsRun: P1TestsRun86 P1TestsRunLLC P1TestsRunLLI

P1TestsRun86: $(P1TESTDIFFS86)
	cat $^

P1TestsRunLLC: $(P1TESTDIFFSLLC)
	cat $^

P1TestsRunLLI: $(P1TESTDIFFSLLI)
	cat $^

P2TestsRun: P2TestsRun86 P2TestsRunLLC P2TestsRunLLI

P2TestsRun86: $(P2TESTDIFFS86)
	cat $^

P2TestsRunLLC: $(P2TESTDIFFSLLC)
	cat $^

P2TestsRunLLI: $(P2TESTDIFFSLLI)
	cat $^

P3TestsRun: P3TestsRun86 P3TestsRunLLC P3TestsRunLLI

P3TestsRun86: $(P3TESTDIFFS86)
	cat $^

P3TestsRunLLC: $(P3TESTDIFFSLLC)
	cat $^

P3TestsRunLLI: $(P3TESTDIFFSLLI)
	cat $^

PXTestsRun: PXTestsRun86 PXTestsRunLLC PXTestsRunLLI

PXTestsRun86: $(PXTESTDIFFS86)
	cat $^

PXTestsRunLLC: $(PXTESTDIFFSLLC)
	cat $^

PXTestsRunLLI: $(PXTESTDIFFSLLI)
	cat $^

$(TESTDIFFS86): $(BUILDDIR)%.86diff: $(BUILDDIR)%.86out $(TESTDIR)%.in
	cat $(TESTDIR)$*.in | $(BUILDDIR)$*.86out > $(BUILDDIR)$*.86output
	cat $(TESTDIR)$*.in | $(TESTDIR)$*.py > $(BUILDDIR)$*.correct
	diff -B -s -q $(BUILDDIR)$*.86output $(BUILDDIR)$*.correct > $@

$(BMTESTRT86): $(BENCHDIR)%.86rt: $(TESTDIR)%.py $(TESTDIR)%.in *.py
	$(MAKE) $(BUILDDIR)$*.86out
	cat $(TESTDIR)$*.in | $(TIME) $(TIMEFLAGS) -o $@ $(BUILDDIR)$*.86out > $(NULL)
	$(MAKE) buildclean
	$(MAKE) pycclean

$(BMTESTCT86): $(BENCHDIR)%.86ct: $(TESTDIR)%.py *.py
	$(MAKE) buildclean
	$(MAKE) pycclean
	$(TIME) $(TIMEFLAGS) -o $@ $(MAKE) $(BUILDDIR)$*.86out
	$(MAKE) buildclean
	$(MAKE) pycclean

$(TESTDIFFSLLC): $(BUILDDIR)%.llcdiff: $(BUILDDIR)%.llout $(TESTDIR)%.in
	cat $(TESTDIR)$*.in | $(BUILDDIR)$*.llout > $(BUILDDIR)$*.llcoutput
	cat $(TESTDIR)$*.in | $(TESTDIR)$*.py > $(BUILDDIR)$*.correct
	diff -B -s -q $(BUILDDIR)$*.llcoutput $(BUILDDIR)$*.correct > $@

$(BMTESTRTLLC): $(BENCHDIR)%.llcrt: $(TESTDIR)%.py $(TESTDIR)%.in *.py
	$(MAKE) $(BUILDDIR)$*.llout
	cat $(TESTDIR)$*.in | $(TIME) $(TIMEFLAGS) -o $@ $(BUILDDIR)$*.llout > $(NULL)
	$(MAKE) buildclean
	$(MAKE) pycclean

$(BMTESTCTLLC): $(BENCHDIR)%.llcct: $(TESTDIR)%.py *.py
	$(MAKE) buildclean
	$(MAKE) pycclean
	$(TIME) $(TIMEFLAGS) -o $@ $(MAKE) $(BUILDDIR)$*.llout
	$(MAKE) buildclean
	$(MAKE) pycclean

$(TESTDIFFSLLI): $(BUILDDIR)%.llidiff: $(BUILDDIR)%.lbc $(TESTDIR)%.in
	cat $(TESTDIR)$*.in | $(LLI) $(BUILDDIR)$*.lbc > $(BUILDDIR)$*.llioutput
	cat $(TESTDIR)$*.in | $(TESTDIR)$*.py > $(BUILDDIR)$*.correct
	diff -B -s -q $(BUILDDIR)$*.llioutput $(BUILDDIR)$*.correct > $@

$(BMTESTRTLLI): $(BENCHDIR)%.llirt: $(TESTDIR)%.py $(TESTDIR)%.in *.py
	$(MAKE) $(BUILDDIR)$*.lbc
	cat $(TESTDIR)$*.in | $(TIME) $(TIMEFLAGS) -o $@ $(LLI) $(BUILDDIR)$*.lbc > $(NULL)
	$(MAKE) buildclean
	$(MAKE) pycclean

$(BMTESTCTLLI): $(BENCHDIR)%.llict: $(TESTDIR)%.py *.py
	$(MAKE) buildclean
	$(MAKE) pycclean
	$(TIME) $(TIMEFLAGS) -o $@ $(MAKE) $(BUILDDIR)$*.lbc
	$(MAKE) buildclean
	$(MAKE) pycclean

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

clean: buildclean pycclean
	$(RM) *~
	$(RM) $(TESTDIR)*~
	$(RM) $(HELPERDIR)*~
	$(RM) $(BENCHDIR)*
	$(RM) \#*\#
	$(RM) *.s
	$(RM) *.out
	$(RM) *.dot
	$(RM) *.svg
	$(RM) *.jpg
	$(RM) submit.zip
	$(RM) -r $(SUBMISSIONDIR)

pycclean:
	$(RM) *.pyc

buildclean:
	$(RM) $(BUILDDIR)*
