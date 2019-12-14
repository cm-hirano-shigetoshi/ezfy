import subprocess
from subprocess import PIPE


def execute(command):
    proc = subprocess.run(command, shell=True, stdout=PIPE, text=True)
    return proc.stdout


def transform(input_text, command):
    proc = subprocess.run(
        command, shell=True, input=input_text, stdout=PIPE, text=True)
    return proc.stdout


def awk_1(line, delimiter=None):
    if delimiter is None:
        stripped = line.lstrip(' ')
        if '\t' in stripped or ' ' in stripped:
            return stripped[:stripped.replace('\t', ' ').find(' ')]
        else:
            return stripped
    else:
        return line[:line.find(delimiter):]
