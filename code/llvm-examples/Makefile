CLANGLIBS = \
				-lclangTooling\
				-lclangFrontendTool\
				-lclangFrontend\
				-lclangDriver\
				-lclangSerialization\
				-lclangCodeGen\
				-lclangParse\
				-lclangSema\
				-lclangStaticAnalyzerFrontend\
				-lclangStaticAnalyzerCheckers\
				-lclangStaticAnalyzerCore\
				-lclangAnalysis\
				-lclangARCMigrate\
				-lclangRewriteFrontend\
				-lclangRewriteCore\
				-lclangEdit\
				-lclangAST\
				-lclangLex\
				-lclangBasic\
				$(shell llvm-config --libs)

#LLVMCOMPONENTS := llvm-gcc
LLVMCONFIG := llvm-config
LLVMLIBS := $(shell $(LLVMCONFIG) --libs)
LLVMLDFLAGS := $(shell $(LLVMCONFIG) --ldflags --libs)
LLSOURCE = $(wildcard *.ll)
BITCODE_FILES = $(LLSOURCE:.ll=.bc)
ASSEMBLY = $(BITCODE_FILES:.bc=.s)
EXECS = $(ASSEMBLY:.s=)
CC  = gcc
LLC = llc
LLA = llvm-as

# all: $(EXES)

# ${EXES}: $(ASSEMBLY)
# 	gcc -o $@ $^ $(LLVMLIBS) $(LLVMLDFLAGS)

# ${ASSEMBLY}: $(BITCODE_FILES)
# 	llc $<

# ${BITCODE_FILES}: $(LLSOURCE)
# 	llvm-as $<

all: hello0

hello0: hello0.s
	$(CC) -o $@ $^ $(LLVMLIBS) $(LLVMLDFLAGS)

hello0.s: hello0.bc
	$(LLC) hello0.bc

hello0.bc: hello0.ll
	$(LLA) hello0.ll

clean:
	$(RM) *.bc *.s $(EXECS)
