class Continue():
    def __init__(self, continues):
        self.__continues = continues

    def get_expect(self):
        return list(self.__continues.keys())

