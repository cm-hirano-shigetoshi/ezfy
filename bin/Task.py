from Opts import Opts
from Bind import Bind
from Stdout import Stdout


class Task():
    def __init__(self, yml, continue_expect):
        self.__yml = yml
        self.__set_input(yml['input'])
        self.__preview = ''
        self.__set_preview(yml.get('preview', ''))
        self.__opts = None
        self.__set_opts(yml.get('opts', []))
        self.__bind = None
        self.__set_bind(yml.get('bind', {}))
        self.__stdout = None
        self.__set_stdout(yml.get('stdout', {}))
        self.__continue_expect = continue_expect

    def __get_input(self):
        return self.__input

    def __get_opts(self):
        return self.__opts.to_string()

    def __get_preview(self):
        if len(self.__preview) > 0:
            return '--preview="{}"'.format(self.__preview)
        else:
            return ''

    def __get_bind(self):
        bind = self.__bind.to_string()
        if len(bind) > 0:
            return '--bind="{}"'.format(self.__bind.to_string())
        else:
            return ''

    def __set_input(self, input):
        if len(input) > 0:
            self.__input = input

    def __set_opts(self, opts):
        if len(opts) > 0:
            if self.__opts is None:
                self.__opts = Opts(opts)
            else:
                self.__opts.set(opts)

    def __set_preview(self, preview):
        self.__preview = preview

    def __set_bind(self, bind):
        if len(bind) > 0:
            if self.__bind is None:
                self.__bind = Bind(bind)
            else:
                self.__bind.set(bind)

    def __set_stdout(self, stdout):
        if len(stdout) > 0:
            if self.__stdout is None:
                self.__stdout = Stdout(stdout)
            else:
                self.__stdout.set(stdout)

    def __get_expect(self):
        expects = self.__continue_expect + self.__stdout.get_expect()
        if 'enter' not in expects:
            expects.append('enter')
        return '--expect="{}"'.format(','.join(expects))

    def __get_fzf_options(self):
        return '{} {} {} {}'.format(self.__get_opts(), self.__get_preview(),
                                    self.__get_bind(), self.__get_expect())

    def get_cmd(self):
        cmd = '{} | fzf {}'.format(self.__get_input(), self.__get_fzf_options())
        return cmd

    def stdout(self, result):
        key = result.split('\n')[1]
        content = '\n'.join(result.split('\n')[2:])
        self.__stdout.write(key, content)

    def is_continue(self, result):
        key = result.split('\n')[1]
        return key in self.__continue_expect

    def create_continue_task(self, continue_dict):
        new_task = Task(self.__yml, self.__continue_expect)
        new_task.__set_input(continue_dict.get('input', ''))
        new_task.__set_opts(continue_dict.get('opts', []))
        new_task.__set_preview(continue_dict.get('preview', ''))
        new_task.__set_bind(continue_dict.get('bind', {}))
        new_task.__set_stdout(continue_dict.get('stdout', {}))
        return new_task
