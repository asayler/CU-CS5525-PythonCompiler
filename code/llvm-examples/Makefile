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
LLVMLIBS := $(shell llvm-config --libs)
LLVMLDFLAGS := $(shell $(LLVMCONFIG) --ldflags --libs)
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

all: hello0

hello0: hello0.s
	gcc -o $@ $^ $(LLVMLIBS) $(LLVMLDFLAGS)
hello0.s: hello0.bc
	llc hello0.bc
hello0.bc: hello0.ll
	llvm-as hello0.ll

clean:
	rm *.bc *.s $(EXECS)