import re
import Command
from Temporary import Temporary


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
                list(
                    map(lambda l: Output.awk_1(l, transform.get_delimiter()),
                        content.split('\n'))))
            line_selector = self.__variables.expand(
                "{tooldir}/main/line_selector.pl")
            content = Command.execute('cat {} | {} "{}"'.format(
                Temporary.temp_path('transform'), line_selector, indexes))
        if key == 'enter' and key not in self.__output:
            print(re.sub('\n$', '', content))
        else:
            for ope_dict in self.__output[key]:
                for ope, value in ope_dict.items():
                    if ope == 'pipe':
                        command = self.__variables.expand(value)
                        content = Command.transform(content, command)
            print(re.sub('\n$', '', content))

    def set(self, output):
        self.__output = output

    def awk_1(line, delimiter=None):
        if delimiter is None:
            stripped = line.lstrip(' ')
            if '\t' in stripped or ' ' in stripped:
                return stripped[:stripped.replace('\t', ' ').find(' ')]
            else:
                return stripped
        else:
            return line[:line.find(delimiter):]
