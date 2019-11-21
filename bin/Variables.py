class Variables():
    def __init__(self, args):
        self.__pyscript = args[0]
        self.__subcmd = args[1]
        self.__yml = args[2]
        self.__args = args[3:]

    def expand(self, text):
        text = self.expand_tool_vars(text)
        text = self.expand_args(text)
        return text

    def expand_tool_vars(self, text):
        text = text.replace('$yml', self.__yml)
        return text

    def expand_args(self, text):
        for i in range(9):
            if i >= len(self.__args):
                break
            text = text.replace('$arg{}'.format(str(i+1)), self.__args[i])
        return text

