#!/usr/bin/env python
import sys
import re
from signal import signal, SIGPIPE, SIG_DFL
import argparse
signal(SIGPIPE, SIG_DFL)
p = argparse.ArgumentParser()
p.add_argument('start')
p.add_argument('end')
p.add_argument('-F', '--delimiter')
args = p.parse_args()

start = int(args.start)
start = start - 1 if start > 0 else start
end = int(args.end)
end = end - 1 if end > 0 else end
line = sys.stdin.readline()
while line:
    line = line.strip("\n")
    if args.delimiter is None:
        pattern = r'\S+'
    else:
        pattern = r'[^{}]+'.format(args.delimiter)
    array = [m for m in re.finditer(pattern, line)]
    pos_start = array[start].start()
    pos_end = array[end].end()
    print(line[pos_start:pos_end].strip(r'\t '))
    line = sys.stdin.readline()

