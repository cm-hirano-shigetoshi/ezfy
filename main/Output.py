import re
import Command


class Output():
    def __init__(self, output, variables):
        self.__output = {}
        self.__variables = variables
        self.set(output)

    def get_expect(self):
        return list(self.__output.keys())

    def write(self, result):
        if result.key == 'enter' and result.key not in self.__output:
            print(re.sub('\n$', '', result.get_content()))
        else:
            content = result.get_content()
            for ope_dict in self.__output[result.key]:
                for ope, value in ope_dict.items():
                    if ope == 'pipe':
                        command = self.__variables.expand(value)
                        content = Command.transform(content, command)
            print(re.sub('\n$', '', content))

    def set(self, output):
        self.__output = output
