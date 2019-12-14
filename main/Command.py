import subprocess
from subprocess import PIPE


def execute(command):
    proc = subprocess.run(command, shell=True, stdout=PIPE, text=True)
    return proc.stdout


def transform(input_text, command):
    proc = subprocess.run(
        command, shell=True, input=input_text, stdout=PIPE, text=True)
    return proc.stdout
