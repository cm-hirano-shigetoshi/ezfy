class Switch():
    def __init__(self, switch, variables):
        self.__switch = switch
        self.__variables = variables

    def get_expect(self):
        return list(self.__switch.keys())

    def get(self, key, default={}):
        if key in self.__switch:
            return self.__switch[key]
        else:
            return default
