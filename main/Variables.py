from os.path import dirname
import re
from Output import Output
from Transform import Transform


class Variables():
    def __init__(self, args):
        self.pyscript = args[0]
        self.subcmd = args[1]
        self.yml = args[2]
        self.args = args[3:]
        self.vars = ['' for x in range(9)]
        self.__pre_query = ""
        self.__pre_key = ""
        self.__pre_content = ""

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
        m = re.search(r'({arg([1-9])})', text)
        if m is not None:
            index = int(m.group(2)) - 1
            text = text.replace(m.group(1), self.args[index])
        return text

    def expand_vars(self, text):
        m = re.search(r'({var([1-9])})', text)
        if m is not None:
            index = int(m.group(2)) - 1
            text = text.replace(m.group(1), self.vars[index])
        m = re.search(r'({var([1-9])\|([^\|]*)\|([^}]*)})', text)
        if m is not None:
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

    def __get_pre_content(self):
        if '\n' in re.sub('\n$', '', self.__pre_content):
            return self.__pre_content
        else:
            return self.__pre_content[:-1]

    def set_vars(self, var):
        for v in var:
            for key, val in v.items():
                m = re.match('^var([1-9])', key)
                self.vars[int(m.group(1)) - 1] = self.expand(val)

    def set_pre(self, result, transform):
        if transform.exists():
            self.__pre_query = result.split('\n')[0]
            self.__pre_key = result.split('\n')[1]
            indexes = ','.join(
                list(map(lambda l: Output.awk_1(l),
                         result.split('\n')[2:])))
            line_selector = self.expand("{tooldir}/main/line_selector.pl")
            content = Output.pipe(
                '', 'cat {} | {} "{}"'.format(Transform.get_temp_name(),
                                              line_selector, indexes))
            self.__pre_content = content
        else:
            self.__pre_query = result.split('\n')[0]
            self.__pre_key = result.split('\n')[1]
            self.__pre_content = '\n'.join(result.split('\n')[2:])

    def pop_1(line):
        line = line.replace('\t', ' ').lstrip(' ')
        replaced_line = line
        if ' ' not in replaced_line.rstrip(' '):
            return ''
        else:
            return line[replaced_line.find(' '):].lstrip()
