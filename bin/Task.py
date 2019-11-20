import yaml
from Options import Options
from Binds import Binds


class Task():
    def __init__(self, yml=None):
        if yml is not None:
            with open(yml) as f:
                self.__yml = yaml.load(f, Loader=yaml.SafeLoader)['base_task']

    def __get_fzf_app(self):
        return self.__yml.get('fzf', 'fzf')

    def __get_input(self):
        return self.__yml['input']

    def __get_opts(self):
        opts = Options(self.__yml.get('opts', []))
        return opts.get_opts_string()

    def __get_preview(self):
        if 'preview' not in self.__yml:
            return ''
        return '--preview="{}"'.format(self.__yml['preview'])

    def __get_binds(self):
        binds = Binds(self.__yml.get('binds', []))
        bind_string = binds.get_binds_string()
        if len(bind_string) == 0:
            return ''
        else:
            return '--bind="{}"'.format(bind_string)

    def __get_fzf_options(self):
        return '{} {} {}'.format(self.__get_opts(), self.__get_preview(), self.__get_binds())

    def get_cmd(self):
        cmd = '{} | {} {}'.format(self.__get_input(), self.__get_fzf_app(), self.__get_fzf_options())
        return cmd
