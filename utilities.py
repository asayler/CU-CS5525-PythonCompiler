#!/usr/bin/python

# Andy Sayler
# Fall 2012
# CU CS5525
# utility functions
#
# Adopted from Jeremy Siek, Fall 2012
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

counter = 0

def generate_name(x):
    global counter
    name = str(counter) + '_' + x
    counter = counter + 1
    return name
