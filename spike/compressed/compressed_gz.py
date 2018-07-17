#! /usr/bin/env python3.6
import gzip
import sys

# with gzip.open('passed1.vcf.gz','r') as f:
    # for line in f:
        # print(line.decode('UTF-8'),end = '')

# with open('passed1.vcf.gz','rb') as f:
with sys.stdin as f:
    i = 0
    for line in f:
        print(line)
        i+=1
    print('len is ',i)

