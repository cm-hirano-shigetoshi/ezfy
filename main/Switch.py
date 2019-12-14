class Switch():
    def __init__(self, switch_dict, variables):
        self.__switch_dict = switch_dict
        self.__variables = variables

    def get_expect(self):
        return list(self.__switch_dict.keys())

    def get(self, key, default={}):
        if key in self.__switch_dict:
            return self.__switch_dict[key]
        else:
            return default

    def has(self, key):
        return key in self.__switch_dict
