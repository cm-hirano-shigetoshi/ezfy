from Opts import Opts
from Bind import Bind
from Stdout import Stdout


class Task():
    def __init__(self, yml, continue_expect=[]):
        self.__yml = yml
        self.__input = yml['input']
        self.__fzf = yml.get('fzf', 'fzf')
        self.__opts = Opts(yml.get('opts', []))
        self.__preview = yml.get('preview' '')
        self.__bind = Bind(yml.get('bind', {}))
        self.__stdout = Stdout(yml.get('stdout', {}))
        self.__continue_expect = continue_expect

    def __get_input(self):
        return self.__input

    def __get_fzf_app(self):
        return self.__fzf

    def __get_opts(self):
        return self.__opts.to_string()

    def __get_preview(self):
        return '--preview="{}"'.format(self.__preview)

    def __get_bind(self):
        return '--bind="{}"'.format(self.__bind.to_string())

    def __set_input(self, continue_dict):
        if 'input' in continue_dict:
            self.__input = continue_dict['input']

    def __set_opts(self, continue_dict):
        if 'opts' in continue_dict:
            self.__opts.set(continue_dict['opts'])

    def __set_preview(self, continue_dict):
        if 'preview' in continue_dict:
            self.__preview = continue_dict['preview']

    def __set_bind(self, continue_dict):
        if 'bind' in continue_dict:
            self.__bind.set(continue_dict['bind'])

    def __set_stdout(self, continue_dict):
        if 'stdout' in continue_dict:
            self.__stdout.set(continue_dict['stdout'])

    def __get_expect(self):
        expects = ','.join(self.__continue_expect + self.__stdout.get_expect())
        return '--expect="{}"'.format(expects)

    def __get_fzf_options(self):
        return '{} {} {} {}'.format(self.__get_opts(), self.__get_preview(),
                                    self.__get_bind(), self.__get_expect())

    def get_cmd(self):
        cmd = '{} | {} {}'.format(self.__get_input(), self.__get_fzf_app(),
                                  self.__get_fzf_options())
        return cmd

    def stdout(self, result):
        key = result.split('\n')[1]
        content = '\n'.join(result.split('\n')[2:])
        self.__stdout.write(key, content)

    def is_continue(self, result):
        key = result.split('\n')[1]
        return key in self.__continue_expect

    def create_continue_task(self, continue_dict):
        new_task = Task(self.__yml)
        new_task.__set_input(continue_dict)
        new_task.__set_opts(continue_dict)
        new_task.__set_preview(continue_dict)
        new_task.__set_bind(continue_dict)
        new_task.__set_stdout(continue_dict)
        return new_task
