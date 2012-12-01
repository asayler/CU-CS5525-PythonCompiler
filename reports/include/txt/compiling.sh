# Compile all C helper files to LLVM; emits .bc bitcode files
clang -emit-llvm -o runtime.bc           -S runtime.c
clang -emit-llvm -o hashtable.bc         -S hashtable.c
clang -emit-llvm -o hashtable_itr.bc     -S hashtable_itr.c
clang -emit-llvm -o hashtable_utility.bc -S hashtable_utility.c

# Convert a LLVM test file emitted from our compiler to bitcode
llvm-as test.ll

# Link all bitcode files
llvm-link test.bc $ALL_RUNTIME_BC_FILES -o test-linked.bc

# At this juncture, one can either run:
if $INTERPRETER; then
    # To run in the interpreter
    lli test-linked.bc
else
    # To compile to .s code for the local platform
    llc test-linked.bc
    # And output the executable
    clang test-linked.s -o test
fi
