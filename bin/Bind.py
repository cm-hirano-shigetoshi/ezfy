class Bind():
    def __init__(self, binds):
        self.__binds = {}
        for key, command in binds.items():
            self.__binds[key] = self.__split_commands(command)

    def __split_commands(self, command):
        # TODO
        # executeの中などに"+"が入っていた場合を考慮する必要がある
        return command.split('+')

    def to_string(self):
        binds_array = []
        for key, commands in self.__binds.items():
            binds_array.append('{}:{}'.format(key, '+'.join(commands)))
        return ','.join(binds_array)

    def set(self, binds):
        for key, command in binds.items():
            self.__binds[key] = self.__split_commands(command)

