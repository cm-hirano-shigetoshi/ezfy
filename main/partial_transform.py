import os
import sys
import re
import argparse
import subprocess
from subprocess import PIPE

p = argparse.ArgumentParser()
p.add_argument('nth', type=int, help='nth')
p.add_argument('command', help='command')
p.add_argument('-F', '--delimiter', help='default: awk style')
p.add_argument('--sync', action='store_true', help='synchronous output')
p.add_argument('--bufferN', type=int, default=1000, help='flush each N line')
args = p.parse_args()


def get_parts(line):
    if args.delimiter is not None:
        pattern = r'[^{}]+'.format(args.delimiter)
    else:
        pattern = r'\S+'
    if args.nth == 0:
        return ('', line, '')
    elif args.nth > 0:
        count = 0
        for m in re.finditer(pattern, line):
            count += 1
            if count >= args.nth:
                left = line[:m.start()]
                target = m.group(0)
                right = line[m.end():]
                return (left, target, right, False)
    elif args.nth < 0:
        matches = []
        for m in re.finditer(pattern, line):
            matches.append(m)
        if len(matches) >= -args.nth:
            m = matches[len(matches) + args.nth]
            left = line[:m.start()]
            target = m.group(0)
            right = line[m.end():]
            return (left, target, right, False)
    return ('', line, '', True)


def shell_command(lines, command):
    input_text = '\n'.join(lines)
    proc = subprocess.run(
        command, shell=True, input=input_text, stdout=PIPE, text=True)
    return proc.stdout.split('\n')


def flush(left, target, right, asis):
    transformed = shell_command(target, args.command)
    for i in range(len(left)):
        if asis[i]:
            print('{}{}{}'.format(left[i], target[i], right[i]))
        else:
            print('{}{}{}'.format(left[i], transformed[i], right[i]))


try:
    line = sys.stdin.readline()
    left_lines = []
    target_lines = []
    right_lines = []
    asis_lines = []
    while line:
        line = line.strip('\n')
        (left, target, right, asis) = get_parts(line)
        left_lines.append(left)
        target_lines.append(target)
        right_lines.append(right)
        asis_lines.append(asis)
        if not args.sync and len(target_lines) >= args.bufferN:
            flush(left_lines, target_lines, right_lines, asis_lines)
            left_lines = []
            target_lines = []
            right_lines = []
        line = sys.stdin.readline()
    flush(left_lines, target_lines, right_lines, asis_lines)
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
