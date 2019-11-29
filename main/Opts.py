class Opts():
    def __init__(self, opts, variables):
        self.__opts = {}
        self.__variables = variables
        self.set(opts)

    def to_string(self):
        opts_array = []
        for key, val in self.__opts.items():
            if type(val) is bool:
                if val:
                    opts_array.append('--{}'.format(key))
                else:
                    opts_array.append('--no-{}'.format(key))
            else:
                opts_array.append('--{}="{}"'.format(key, val))
        opts_array = list(
            map(lambda o: self.__variables.expand(o), opts_array))
        return ' '.join(opts_array)

    def set(self, opts):
        for opt in opts:
            if '=' in opt:
                (key, val) = tuple(opt.split('='))
                if val[0] == "'" and val[-1] == "'":
                    val = val[1:-1]
                elif val[0] == '"' and val[-1] == '"':
                    val = val[1:-1]
                self.__opts[key] = val
            elif opt.startswith('no-'):
                self.__opts[opt[3:]] = False
            else:
                self.__opts[opt] = True
        self.__opts['print-query'] = True

    def set_nth_for_transform(self):
        self.__opts['with-nth=2..'] = True

    def get(self, key, default=None):
        if key in self.__opts:
            return self.__opts[key]
        else:
            return default
