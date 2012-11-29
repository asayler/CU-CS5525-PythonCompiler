LLVMCONFIG := llvm-config
LLVMLIBS := $(shell $(LLVMCONFIG) --libs)
LLVMLDFLAGS := $(shell $(LLVMCONFIG) --ldflags --libs)

CC    = gcc
LLC   = llc
LLA   = llvm-as
LLL   = llvm-link
LLCC  = clang

LLSOURCE = $(wildcard *.ll)
BITCODE_FILES = $(LLSOURCE:.ll=.bc)
ASSEMBLY = $(BITCODE_FILES:.bc=.s)
EXECS = $(ASSEMBLY:.s=)

# all: $(EXES)

# ${EXES}: $(ASSEMBLY)
# 	gcc -o $@ $^ $(LLVMLIBS) $(LLVMLDFLAGS)

# ${ASSEMBLY}: $(BITCODE_FILES)
# 	llc $<

# ${BITCODE_FILES}: $(LLSOURCE)
# 	llvm-as $<

all: hello0 hello1

hello0: hello0.s
	$(CC) -o $@ $^ $(LLVMLIBS) $(LLVMLDFLAGS)

hello0.s: hello0.bc
	$(LLC) hello0.bc

hello0.bc: hello0.ll
	$(LLA) hello0.ll

hello1: hello1.s
	$(LLCC) hello1.s -o hello1

hello1.s: hello1-aug.bc
	$(LLC) hello1-aug.bc -o hello1.s	

hello1-aug.bc: hello1.bc ref1.bc
	$(LLL) hello1.bc ref1.bc -o hello1-aug.bc

ref1.bc: ref1.c
	$(LLCC) -emit-llvm -S ref1.c -o ref1.bc

hello1.bc: hello1.ll
	$(LLA) hello1.ll

clean:
	$(RM) *.bc *.s $(EXECS)
