import re
import subprocess
from subprocess import PIPE
from Transform import Transform


class Stdout():
    def __init__(self, stdout, variables):
        self.__stdout = {}
        self.__variables = variables
        self.set(stdout)

    def get_expect(self):
        return list(self.__stdout.keys())

    def write(self, query, key, content):
        if key == 'enter' and key not in self.__stdout:
            print(re.sub('\n$', '', content))
        else:
            for ope_dict in self.__stdout[key]:
                for ope, value in ope_dict.items():
                    if ope == 'before-transformed':
                        if value == 'LINE' or True:
                            line_selector = self.__variables.expand(
                                "{tooldir}/bin/line_selector.pl")
                            indexes = ','.join(
                                list(map(lambda l: Stdout.awk_1(l), content.split('\n'))))
                            content = Stdout.pipe(
                                '', 'cat {} | {} "{}"'.format(
                                    Transform.get_temp_name(), line_selector,
                                    indexes))
                    elif ope == 'pipe':
                        command = self.__variables.expand(value)
                        content = Stdout.pipe(content, command)
            print(re.sub('\n$', '', content))

    def pipe(input_text, command):
        proc = subprocess.run(
            command, shell=True, input=input_text, stdout=PIPE, text=True)
        return proc.stdout

    def set(self, stdout):
        self.__stdout = stdout

    def awk_1(line):
        stripped = line.lstrip(' ')
        if '\t' in stripped or ' ' in stripped:
            return stripped[:stripped.replace('\t', ' ').find(' ')]
        else:
            return stripped
