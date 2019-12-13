import os
import sys
import re
import argparse
import subprocess
from subprocess import PIPE

p = argparse.ArgumentParser()
p.add_argument('nth', type=int, help='nth')
p.add_argument('command', help='command')
p.add_argument('-F', '--delimiter', default=' ', help='default: space')
args = p.parse_args()

def get_parts(line):
    count = 0
    for m in re.finditer(r'[^{}]+'.format(args.delimiter), line):
        count += 1
        if count >= args.nth:
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
    transformed = shell_command(target, args.command)
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
    flush(left_lines, target_lines, right_lines)
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
