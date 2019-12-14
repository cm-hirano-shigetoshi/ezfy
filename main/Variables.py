from os.path import dirname, abspath
import re


class Variables():
    def __init__(self, args):
        self.pyscript = abspath(args[0])
        self.subcmd = args[1]
        self.yml = abspath(args[2])
        self.args = args[3:]
        self.vars = ['' for x in range(9)]
        self.__pre_query = ""
        self.__pre_key = ""
        self.__pre_content = ""

    def set_vars(self, var):
        for v in var:
            for key, val in v.items():
                m = re.match('^var([1-9])', key)
                self.vars[int(m.group(1)) - 1] = self.expand(val)

    def expand(self, text):
        text = self.expand_tool_vars(text)
        text = self.expand_args(text)
        text = self.expand_vars(text)
        text = self.expand_pre(text)
        return text

    def expand_tool_vars(self, text):
        text = text.replace('{tooldir}', dirname(dirname(self.pyscript)))
        text = text.replace('{ymldir}', dirname(self.yml))
        text = text.replace('{yml}', self.yml)
        return text

    def expand_args(self, text):
        for m in re.finditer(r'({arg([1-9])})', text):
            index = int(m.group(2)) - 1
            text = text.replace(m.group(1), self.args[index])
        return text

    def expand_vars(self, text):
        for m in re.finditer(r'({var([1-9])})', text):
            index = int(m.group(2)) - 1
            text = text.replace(m.group(1), self.vars[index])
        for m in re.finditer(r'({var([1-9])\|([^\|]*)\|([^}]*)})', text):
            index = int(m.group(2)) - 1
            replaced = m.group(4) if self.vars[index] == m.group(
                3) else m.group(3)
            text = text.replace(m.group(1), replaced)
        return text

    def expand_pre(self, text):
        text = text.replace('{pre_query}', self.__pre_query)
        text = text.replace('{pre_key}', self.__pre_key)
        text = text.replace('{pre_content}', self.__get_pre_content())
        return text

    def set_pre(self, result):
        self.__pre_query = result.query
        self.__pre_key = result.key
        self.__pre_content = result.get_content()

    def __get_pre_content(self):
        if '\n' in re.sub('\n$', '', self.__pre_content):
            return self.__pre_content
        else:
            return self.__pre_content[:-1]
