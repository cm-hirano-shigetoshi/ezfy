class Bind():
    def __init__(self, bind, variables, transform):
        self.__bind = {}
        self.__variables = variables
        self.__transform = transform
        self.set(bind)

    def __split_commands(self, command):
        # TODO
        # executeの中などに"+"が入っていた場合を考慮する必要がある
        return command.split('+')

    def to_string(self):
        bind_array = []
        for key, commands in self.__bind.items():
            for i in range(len(commands)):
                c = commands[i]
                if c.startswith('execute') or c.startswith('reload'):
                    if not self.__transform.is_empty():
                        c = self.__transform.adjust_preview(c)
                    c = self.__variables.expand(c)
                commands[i] = c
            bind_array.append('{}:{}'.format(key, '+'.join(commands)))
        return ','.join(bind_array)

    def set(self, bind):
        for key, command in bind.items():
            self.__bind[key] = self.__split_commands(command)
