import re
import subprocess
from subprocess import PIPE


class Stdout():
    def __init__(self, stdout, variables):
        self.__stdout = {}
        self.__variables = variables
        self.set(stdout)

    def get_expect(self):
        return list(self.__stdout.keys())

    def write(self, key, content):
        if key == 'enter' and key not in self.__stdout:
            print(re.sub('\n$', '', content))
        else:
            for ope_dict in self.__stdout[key]:
                for ope, command in ope_dict.items():
                    if ope == 'pipe':
                        command = self.__variables.expand(command)
                        content = Stdout.pipe(content, command)
            print(re.sub('\n$', '', content))

    def pipe(input_text, command):
        proc = subprocess.run(
            command, shell=True, input=input_text, stdout=PIPE, text=True)
        return proc.stdout

    def set(self, stdout):
        self.__stdout = stdout
