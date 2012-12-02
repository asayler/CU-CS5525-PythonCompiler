#include "runtime.h"

void test(){

    pyobj po;
    big_pyobj* bpo;

    po = input_int();
    print_any(po);
    bpo = project_big(po);
    po  = inject_big(bpo);

}
