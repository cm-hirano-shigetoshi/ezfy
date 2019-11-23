import os


class Variables():
    def __init__(self, args):
        self.__pyscript = args[0]
        self.__subcmd = args[1]
        self.__yml = args[2]
        self.__args = args[3:]
        self.__pre_query = ""
        self.__pre_key = ""
        self.__pre_content = ""

    def expand(self, text):
        text = self.expand_tool_vars(text)
        text = self.expand_args(text)
        text = self.expand_pre(text)
        return text

    def expand_tool_vars(self, text):
        text = text.replace('{ymldir}', os.path.dirname(self.__yml))
        text = text.replace('{yml}', self.__yml)
        return text

    def expand_args(self, text):
        for i in range(9):
            if i >= len(self.__args):
                break
            text = text.replace('{' + 'arg{}'.format(str(i + 1)) + '}',
                                self.__args[i])
        return text

    def expand_pre(self, text):
        text = text.replace('{pre_query}', self.__pre_query)
        text = text.replace('{pre_key}', self.__pre_key)
        text = text.replace('{pre_content}', self.__pre_content)
        return text

    def set_pre(self, result):
        self.__pre_query = result.split('\n')[0]
        self.__pre_key = result.split('\n')[1]
        self.__pre_content = '\n'.join(result.split('\n')[2:])
