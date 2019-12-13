import os
import sys
import re
import argparse
import subprocess
from subprocess import PIPE

p = argparse.ArgumentParser()
#p.add_argument('arg1', help='引数です')
p.add_argument('-a', '--opt_a', help='オプションです')
p.add_argument('-b', '--opt_b', default='aiueo', help='オプションです')
p.add_argument('-c', '--opt_c', default=0.1, type=float)
p.add_argument('-d', '--opt_d', action='store_true')
args = p.parse_args()

delimtier = '/'

def get_parts(line):
    count = 0
    for m in re.finditer(r'[^{}]+'.format(delimtier), line):
        count += 1
        if count == 2:
            left = line[:m.start()]
            target = m.group(0)
            right = line[m.end():]
            return (left, target, right)
    return (line, '', '')

def shell_command(input_text, command):
    proc = subprocess.run(command, shell=True, input=input_text, stdout=PIPE, text=True)
    return re.sub(r'[\r\n]$', '', proc.stdout)

try:
    line = sys.stdin.readline()
    while line:
        line = line.strip('\n')
        (left, target, right) = get_parts(line)
        transformed = shell_command(target, 'cat -n')
        line = '{}{}{}'.format(left, transformed, right)
        print(line)
        line = sys.stdin.readline()
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
