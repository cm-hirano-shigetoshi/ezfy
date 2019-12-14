class Result():
    def __init__(self, result_text, transform):
        self.query = result_text.split('\n')[0]
        self.key = result_text.split('\n')[1]
        self.__content = '\n'.join(result_text.split('\n')[2:])
        self.__transform = transform

    def is_empty(self):
        return len(self.__content) == 0

    def get_content(self):
        if self.__transform.is_empty():
            return self.__content
        else:
            return self.__transform.get_original_content(self.__content)
