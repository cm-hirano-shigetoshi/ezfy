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
command = 'cat -n'

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

def shell_command(lines, command):
    input_text = '\n'.join(lines)
    proc = subprocess.run(command, shell=True, input=input_text, stdout=PIPE, text=True)
    return proc.stdout.split('\n')

def flush(left, target, right):
    transformed = shell_command(target, command)
    for i in range(len(left)):
        print('{}{}{}'.format(left[i], transformed[i], right[i]))

try:
    line = sys.stdin.readline()
    left_lines = []
    target_lines = []
    right_lines = []
    while line:
        line = line.strip('\n')
        (left, target, right) = get_parts(line)
        left_lines.append(left)
        target_lines.append(target)
        right_lines.append(right)
        if len(target_lines) > 1000:
            flush(left_lines, target_lines, right_lines)
            left_lines = []
            target_lines = []
            right_lines = []
        line = sys.stdin.readline()
    flush()
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
