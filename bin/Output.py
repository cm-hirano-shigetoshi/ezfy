import re
import subprocess
from subprocess import PIPE
from Transform import Transform


class Output():
    def __init__(self, output, variables):
        self.__output = {}
        self.__variables = variables
        self.set(output)

    def get_expect(self):
        return list(self.__output.keys())

    def write(self, query, key, content, transform):
        if transform.exists():
            indexes = ','.join(
                list(map(lambda l: Output.awk_1(l), content.split('\n'))))
            line_selector = self.__variables.expand(
                "{tooldir}/bin/line_selector.pl")
            content = Output.pipe(
                '', 'cat {} | {} "{}"'.format(Transform.get_temp_name(),
                                              line_selector, indexes))
        if key == 'enter' and key not in self.__output:
            print(re.sub('\n$', '', content))
        else:
            for ope_dict in self.__output[key]:
                for ope, value in ope_dict.items():
                    if ope == 'pipe':
                        command = self.__variables.expand(value)
                        content = Output.pipe(content, command)
            print(re.sub('\n$', '', content))

    def pipe(input_text, command):
        proc = subprocess.run(
            command, shell=True, input=input_text, stdout=PIPE, text=True)
        return proc.stdout

    def set(self, output):
        self.__output = output

    def awk_1(line):
        stripped = line.lstrip(' ')
        if '\t' in stripped or ' ' in stripped:
            return stripped[:stripped.replace('\t', ' ').find(' ')]
        else:
            return stripped
