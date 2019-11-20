import re
from Opts import Opts
from Bind import Bind
from Stdout import Stdout
import subprocess
from subprocess import PIPE



class Task():
    def __init__(self, yml, expect):
        self.__input = yml['input']
        self.__fzf = yml.get('fzf', 'fzf')
        self.__opts = Opts(yml.get('opts', []))
        self.__preview = yml.get('preview' '')
        self.__bind = Bind(yml.get('bind', {}))
        self.__stdout = Stdout(yml.get('stdout', {}))
        self.__expect = expect
        self.__expect.extend(self.__stdout.get_expect())


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

    def __get_expect(self):
        return '--expect="{}"'.format(','.join(self.__expect))

    def __get_fzf_options(self):
        return '{} {} {} {}'.format(self.__get_opts(), self.__get_preview(), self.__get_bind(), self.__get_expect())

    def get_cmd(self):
        cmd = '{} | {} {}'.format(self.__get_input(), self.__get_fzf_app(), self.__get_fzf_options())
        return cmd

    def stdout(self, result):
        key = result.split('\n')[1]
        content = '\n'.join(result.split('\n')[2:])
        self.__stdout.write(key, content)

#    def create_continue_task(self, key):
#        new_task = Task(self.__yml)
#        operations = self.__expects.get_operation(key)
#
#    def is_loop_end(self, result):
#        return True
#        key = result.split('\n')[1]
#        return 'continue' not in self.__expects.get_operation(key)
#
#    def format_output_string(result):
#        stdout = '\n'.join(result.split('\n')[2:])
#        return re.sub('\n$', '', stdout)

