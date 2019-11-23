class Opts():
    def __init__(self, opts, variables):
        self.__opts = {}
        self.__variables = variables
        self.set(opts)

    def to_string(self):
        opts_array = []
        for opt, b in self.__opts.items():
            if b:
                opts_array.append('--{}'.format(opt))
            else:
                opts_array.append('--no-{}'.format(opt))
        opts_array = list(map(lambda o: self.__variables.expand(o), opts_array))
        return ' '.join(opts_array)

    def set(self, opts):
        for opt in opts:
            if opt.startswith('no-'):
                self.__opts[opt[3:]] = False
            else:
                self.__opts[opt] = True
        self.__opts['print-query'] = True
