class Bind():
    def __init__(self, bind):
        self.__bind = {}
        self.set(bind)

    def __split_commands(self, command):
        # TODO
        # executeの中などに"+"が入っていた場合を考慮する必要がある
        return command.split('+')

    def to_string(self):
        bind_array = []
        for key, commands in self.__bind.items():
            bind_array.append('{}:{}'.format(key, '+'.join(commands)))
        return ','.join(bind_array)

    def set(self, bind):
        for key, command in bind.items():
            self.__bind[key] = self.__split_commands(command)
