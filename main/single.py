#!/usr/bin/env python
import sys
import re
from signal import signal, SIGPIPE, SIG_DFL
import argparse
signal(SIGPIPE, SIG_DFL)
p = argparse.ArgumentParser()
p.add_argument('index')
p.add_argument('-F', '--delimiter')
args = p.parse_args()

index = int(args.index)
index = index - 1 if index > 0 else index
line = sys.stdin.readline()
while line:
    line = line.strip("\n")
    if args.delimiter is None:
        if index >= 0:
            i = 0
            for m in re.finditer(r'\S+', line.strip()):
                if i == index:
                    print(m.group(0))
                    break
                i += 1
        else:
            array = []
            for m in re.finditer(r'\S+', line.strip()):
                array.append(m.group(0))
            print(array[index])
    else:
        print(line.split(args.delimiter)[index])
    line = sys.stdin.readline()
