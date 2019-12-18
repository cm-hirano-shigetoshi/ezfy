#!/usr/bin/env python
import os
import sys
import re
import subprocess
import argparse
import tempfile

p = argparse.ArgumentParser()
p.add_argument('nth', type=int, help='nth')
p.add_argument('command', help='command')
p.add_argument('-F', '--delimiter', help='default: awk style')
args = p.parse_args()

if args.delimiter is not None and len(args.delimiter) > 1:
    print('[Error] Delimiter must be ONE character', file=sys.stderr)
    sys.exit(1)

try:

    def get_parts(line, pattern):
        if args.nth == 0:
            return ('', line, '')
        elif args.nth > 0:
            count = 0
            if args.delimiter is None:
                for m in re.finditer(pattern, line):
                    count += 1
                    if count >= args.nth:
                        left = line[:m.start()]
                        target = m.group(0)
                        right = line[m.end():]
                        return (left, target, right)
                return (line, '', '')
            else:
                start = 0
                for m in re.finditer(pattern, line + args.delimiter):
                    count += 1
                    if count >= args.nth:
                        left = line[:start]
                        target = line[start:m.start()]
                        right = line[m.start():]
                        return (left, target, right)
                    start = m.end()
                return (line, '', '')
        elif args.nth < 0:
            matches = []
            if args.delimiter is None:
                for m in re.finditer(pattern, line):
                    matches.append(m)
                if len(matches) >= -args.nth:
                    m = matches[len(matches) + args.nth]
                    left = line[:m.start()]
                    target = m.group(0)
                    right = line[m.end():]
                    return (left, target, right)
                return ('', '', line)
            else:
                for m in re.finditer(pattern, line + args.delimiter):
                    matches.append(m)
                if len(matches) >= -args.nth:
                    end = 0
                    if len(matches) + args.nth - 1 >= 0:
                        end = matches[len(matches) + args.nth - 1].end()
                    m = matches[len(matches) + args.nth]
                    left = line[:end]
                    target = line[end:m.start()]
                    right = line[m.start():]
                    return (left, target, right)
                return ('', '', line)

    if len(args.command) > 0:
        if args.delimiter is None:
            pattern = re.compile(r'\S+')
        else:
            pattern = re.compile(r'[{}]'.format(args.delimiter))
        with tempfile.TemporaryDirectory() as tmpdir:
            p1 = os.path.join(tmpdir, 'p1')
            p2 = os.path.join(tmpdir, 'p2')
            os.mkfifo(p1)
            os.mkfifo(p2)
            subprocess.Popen(
                "cat {} | {} | cat -n  > {}".format(p2, args.command, p1),
                shell=True,
                text=True)
            subprocess.Popen(
                "cat {} | python {} 0 ''".format(p1, __file__),
                shell=True,
                stdout=sys.stdout,
                text=True)
            with open(p1, 'w') as p1:
                with open(p2, 'w') as p2:
                    i = 0
                    line = sys.stdin.readline()
                    while line:
                        i += 1
                        parts = get_parts(line.strip('\n'), pattern)
                        # print('{0[0]}|{0[1]}|{0[2]}'.format(parts))
                        print('l:{}\t{}'.format(i, parts[0]), file=p1)
                        print('{}'.format(parts[1]), file=p2)
                        print('r:{}\t{}'.format(i, parts[2]), file=p1)
                        line = sys.stdin.readline()
    else:
        pool = {}
        line = sys.stdin.readline()
        while line:
            line = line.strip('\n')
            if len(line) > 0:
                p = line[0]
                if p == 'l' or p == 'r':
                    i = line[2:line.find('\t')]
                else:
                    p = 'c'
                    line = line.lstrip()
                    i = line[:line.find('\t')]
                line = line[line.find('\t') + 1:]
                if i not in pool:
                    pool[i] = {}
                pool[i][p] = line
                if len(pool[i].keys()) == 3:
                    p = pool.pop(i)
                    print('{}{}{}'.format(p['l'], p['c'], p['r']))
            line = sys.stdin.readline()
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
except KeyboardInterrupt:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
