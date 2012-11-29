LLVMCONFIG := llvm-config
LLVMLIBS := $(shell $(LLVMCONFIG) --libs)
LLVMLDFLAGS := $(shell $(LLVMCONFIG) --ldflags --libs)

CC      = gcc
CCFLAGS = -c -g
CL      = gcc
CLFLAGS = -g

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

LLSOURCE = $(wildcard *.ll)
BITCODE_FILES = $(LLSOURCE:.ll=.bc)
ASSEMBLY = $(BITCODE_FILES:.bc=.s)

EXECS = $(ASSEMBLY:.s=) functioncall1

all: $(EXECS)

hello0: hello0.s
	$(LLCC) $(LLCCFLAGS) -o $@ $^

hello0.s: hello0.bc
	$(LLC) $(LLCFLAGS) -o $@ $<

hello0.bc: hello0.ll
	$(LLA) $(LLAFLAGS) -o $@ $<

hello1: hello1.s
	$(LLCC) $(LLCCFLAGS) -o $@ $<

hello1.s: hello1-aug.bc
	$(LLC) $(LLCFLAGS) -o $@ $<	

hello1-aug.bc: hello1.bc ref1.bc
	$(LLL) $(LLLFLAGS) -o $@ $^

ref1.bc: ref1.c
	$(LLCA) $(LLCAFLAGS) -o $@ -S $<

hello1.bc: hello1.ll
	$(LLA) $(LLAFLAGS) -o $@ $<

functioncall1: functioncall1.o ref1.o
	$(CL) $(CLFLAGS) -o $@ $^

ref1.o: ref1.c ref1.h
	$(CC) $(CCFLAGS) -o $@ $<

functioncall1.o: functioncall1.c ref1.h
	$(CC) $(CCFLAGS) -o $@ $<

clean:
	$(RM) *.bc *.s $(EXECS)
	$(RM) *~
