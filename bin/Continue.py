class Continue():
    def __init__(self, continues, variables):
        self.__continues = continues
        self.__variables = variables

    def get_expect(self):
        return list(self.__continues.keys())

    def get(self, key, default={}):
        if key in self.__continues:
            return self.__continues[key]
        else:
            return default
