import re
import subprocess
from subprocess import PIPE


class Stdout():
    def __init__(self, stdout):
        self.set(stdout)

    def get_expect(self):
        return list(self.__yml.keys())

    def write(self, key, content):
        if key == 'enter' and key not in self.__yml:
            print(re.sub('\n$', '', content))
        else:
            for ope_dict in self.__yml[key]:
                for ope, command in ope_dict.items():
                    if ope == 'pipe':
                        content = Stdout.pipe(content, command)
            print(re.sub('\n$', '', content))

    def pipe(input_text, command):
        proc = subprocess.run(
            command, shell=True, input=input_text, stdout=PIPE, text=True)
        return proc.stdout

    def set(self, stdout):
        self.__yml = stdout
