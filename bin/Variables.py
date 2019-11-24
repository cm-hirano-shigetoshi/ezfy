from os.path import dirname
import re


class Variables():
    def __init__(self, args):
        self.pyscript = args[0]
        self.subcmd = args[1]
        self.yml = args[2]
        self.args = args[3:]
        self.__pre_query = ""
        self.__pre_key = ""
        self.__pre_content = ""

    def expand(self, text):
        text = self.expand_tool_vars(text)
        text = self.expand_args(text)
        text = self.expand_pre(text)
        return text

    def expand_tool_vars(self, text):
        text = text.replace('{tooldir}', dirname(dirname(self.pyscript)))
        text = text.replace('{ymldir}', dirname(self.yml))
        text = text.replace('{yml}', self.yml)
        return text

    def expand_args(self, text):
        for i in range(9):
            if i >= len(self.args):
                break
            text = text.replace('{' + 'arg{}'.format(str(i + 1)) + '}',
                                self.args[i])
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

    def set_pre(self, result):
        self.__pre_query = result.split('\n')[0]
        self.__pre_key = result.split('\n')[1]
        self.__pre_content = '\n'.join(result.split('\n')[2:])
