import tempfile

temp_file = None


class Transform():
    def __init__(self, transform, variables):
        self.__transform = {}
        self.__variables = variables
        self.set(transform)

    def exists(self):
        return len(self.__transform) > 0

    def get_cmd(self):
        for ope_dict in self.__transform:
            for ope, value in ope_dict.items():
                if ope == 'pipe':
                    return value

    def set(self, transform):
        self.__transform = transform

    def get_temp_name():
        global temp_file
        if temp_file is None:
            temp_file = tempfile.NamedTemporaryFile()
        return temp_file.name

    def close_temp_file():
        global temp_file
        if temp_file is not None:
            temp_file.close()
            temp_file = None
