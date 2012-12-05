#include <stdio.h>

int main(){

    fprintf(stdout, "char     : %2.2lu\n", sizeof(char));
    fprintf(stdout, "int      : %2.2lu\n", sizeof(int));
    fprintf(stdout, "long     : %2.2lu\n", sizeof(long));
    fprintf(stdout, "long long: %2.2lu\n", sizeof(long long));

    return 0;

}
