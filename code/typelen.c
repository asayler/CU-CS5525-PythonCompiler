/* CU CS5525
 * Fall 2012
 * GSV Python Compiler
 *
 * typelen.c
 * A simple C program to print the type lengths on a given system
 *
 * Repository:
 *    https://github.com/asayler/CU-CS5525-PythonCompiler
 *
 * By :
 *    Anne Gatchell
 *       http://annegatchell.com/
 *    Andrew (Andy) Sayler
 *       http://www.andysayler.com
 *    Michael (Mike) Vitousek
 *       http://csel.cs.colorado.edu/~mivi2269/
 *
 * Copyright (c) 2012 by Anne Gatchell, Andy Sayler, and Mike Vitousek
 *
 * This file is part of the GSV CS5525 Fall 2012 Python Compiler.
 *
 *    The GSV CS5525 Fall 2012 Python Compiler is free software: you
 *    can redistribute it and/or modify it under the terms of the GNU
 *    General Public License as published by the Free Software
 *    Foundation, either version 3 of the License, or (at your option)
 *    any later version.
 *
 *    The GSV CS5525 Fall 2012 Python Compiler is distributed in the
 *    hope that it will be useful, but WITHOUT ANY WARRANTY; without
 *    even the implied warranty of MERCHANTABILITY or FITNESS FOR A
 *    PARTICULAR PURPOSE.  See the GNU General Public License for more
 *    details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with the GSV CS5525 Fall 2012 Python Compiler.  If not, see
 *    <http://www.gnu.org/licenses/>.
 */

#include <stdio.h>

int main(){

    fprintf(stdout, "char      : %2.2zu\n", sizeof(char));
    fprintf(stdout, "int       : %2.2zu\n", sizeof(int));
    fprintf(stdout, "long      : %2.2zu\n", sizeof(long));
    fprintf(stdout, "long long : %2.2zu\n", sizeof(long long));

    return 0;

}
