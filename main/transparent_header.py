#!/usr/bin/env python
import os
import sys
import subprocess
import argparse
import tempfile

p = argparse.ArgumentParser()
p.add_argument('headN', type=int, help='transparent lines')
p.add_argument('command', help='shell command')
args = p.parse_args()

try:
    sys.stdout.reconfigure(line_buffering=True)
    for i in range(args.headN):
        line = sys.stdin.readline()
        sys.stdout.write(line)

    tmpdir = tempfile.mkdtemp()
    tmp_name = os.path.join(tmpdir, 'fifo')
    print(tmp_name)
    os.mkfifo(tmp_name)
    proc = subprocess.Popen(
        "cat {} | {}".format(tmp_name, args.command),
        shell=True,
        stdout=sys.stdout,
        text=True)
    with open(tmp_name, 'w') as f:
        line = sys.stdin.readline()
        while line:
            f.write(line)
            line = sys.stdin.readline()
    os.remove(tmp_name)
    os.rmdir(tmpdir)
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
except KeyboardInterrupt:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
