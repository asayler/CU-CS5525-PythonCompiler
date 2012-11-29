
LLSOURCE = $(wildcard *.ll)
BITCODE_FILES = $(LLSOURCE:.ll=.bc)
ASSEMBLY = $(BITCODE_FILES:.bc=.s)
EXECS = $(ASSEMBLY:.s=)

CLANG = clang
LLVM-ASSEMB = llvm-as


# all: $(EXES)

# ${EXES}: $(ASSEMBLY)
# 	gcc -o $@ $^ $(LLVMLIBS) $(LLVMLDFLAGS)

# ${ASSEMBLY}: $(BITCODE_FILES)
# 	llc $<

# ${BITCODE_FILES}: $(LLSOURCE)
# 	llvm-as $<

all: hello1

hello: hello1.s
	clang hello1.s -o hello1
hello1.s: hello1-aug.bc
	llc hello1-aug.bc -o hello1.s	
hello1-aug.bc: hello1.bc ref1.bc
	llvm-link hello1.bc ref1.bc -o hello1-aug.bc
ref1.bc: ref1.c
	llvm-gcc -emit-llvm -S ref1.c -o ref1.bc
hello1.bc: hello1.ll
	llvm-as hello1.ll

clean:
	rm *.bc *.s $(EXECS)