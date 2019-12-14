from Opts import Opts
from Bind import Bind
from Output import Output
from Transform import Transform
from Temporary import Temporary


class Task():
    def __init__(self, yml=None, variables=None, switch_expect=None):
        if yml is not None:
            self.__variables = variables

            self.__variables.set_vars(yml.get('vars', []))
            self.__opts = Opts(yml.get('opts', []), variables)
            self.__set_input(yml['input'])
            self.__transform = Transform(
                yml.get('transform', ''), variables, self.__opts)
            self.__query = yml.get('query', '')
            self.__preview = yml.get('preview', '')
            self.__bind = Bind(yml.get('bind', {}), variables)
            self.__output = Output(yml.get('output', {}), variables)

            self.__switch_expect = switch_expect

    def get_transform(self):
        return self.__transform

    def __get_input(self):
        return self.__variables.expand(self.__input)

    def __get_opts(self):
        return self.__opts.to_string()

    def __get_preview(self):
        if len(self.__preview) > 0:
            preview = self.__preview
            if not self.__transform.is_empty():
                preview = self.__transform.adjust_preview(preview)
            preview = self.__variables.expand(preview)
            return "--preview='{}'".format(preview)
        else:
            return ''

    def __get_query(self):
        if len(self.__query) > 0:
            expanded = self.__variables.expand(self.__query)
            return '--query="{}"'.format(expanded)
        else:
            return ''

    def __get_bind(self):
        bind = self.__bind.to_string()
        if len(bind) > 0:
            return '--bind="{}"'.format(self.__bind.to_string())
        else:
            return ''

    #
    # Switching to the new task
    #
    def __set_vars(self, var):
        self.__variables.set_vars(var)

    def __set_input(self, input_text):
        self.__input = input_text

    def __set_opts(self, opts):
        self.__opts.set(opts)

    def __set_query(self, query):
        self.__query = query

    def __set_preview(self, preview):
        self.__preview = preview

    def __set_bind(self, bind):
        self.__bind.set(bind)

    def __set_output(self, output):
        self.__output.set(output)

    def __set_transform(self, transform):
        self.__transform.set(transform)

    def __set_transform_opts(self):
        self.__opts.set_nth_for_transform()

    def __get_expect(self):
        expects = self.__switch_expect + self.__output.get_expect()
        if 'enter' not in expects:
            expects.append('enter')
        return '--expect="{}"'.format(','.join(expects))

    def __get_fzf_options(self):
        return '{} {} {} {} {}'.format(self.__get_opts(), self.__get_query(),
                                       self.__get_preview(), self.__get_bind(),
                                       self.__get_expect())

    def __get_transform_cat_n(self):
        delimiter = self.__opts.get('delimiter', None)
        if delimiter is None:
            return 'cat -n'
        else:
            cat = 'cat -n'
            sed = "sed 's/^\\s*\\([0-9]\\+\\)\\t/\\1{}/'".format(delimiter)
            return '{} | {}'.format(cat, sed)

    def clone(self):
        new_task = Task()
        new_task.__variables = self.__variables
        new_task.__input = self.__input
        new_task.__transform = self.__transform
        new_task.__opts = self.__opts
        new_task.__query = self.__query
        new_task.__preview = self.__preview
        new_task.__bind = self.__bind
        new_task.__output = self.__output
        new_task.__switch_expect = self.__switch_expect
        return new_task

    def get_cmd(self):
        if not self.__transform.is_empty():
            self.__set_transform_opts()
            Temporary.create_temp_file('transform')
            cmd = '{} | tee {} | {} | {} | SHELL=bash fzf {}'.format(
                self.__get_input(), Temporary.temp_path('transform'),
                self.__transform.get_cmd(), self.__get_transform_cat_n(),
                self.__get_fzf_options())
            return cmd
        else:
            cmd = '{} | fzf {}'.format(self.__get_input(),
                                       self.__get_fzf_options())
            return cmd

    def output(self, result):
        self.__output.write(result)

    def create_switch_task(self, switch_dict):
        new_task = self.clone()
        if 'vars' in switch_dict:
            new_task.__set_vars(switch_dict['vars'])
        if 'input' in switch_dict:
            new_task.__set_input(switch_dict['input'])
        if 'transform' in switch_dict:
            new_task.__set_transform(switch_dict['transform'])
        if 'opts' in switch_dict:
            new_task.__set_opts(switch_dict['opts'])
        if 'query' in switch_dict:
            new_task.__set_query(switch_dict['query'])
        else:
            new_task.__set_query('{pre_query}')
        if 'preview' in switch_dict:
            new_task.__set_preview(switch_dict['preview'])
        if 'bind' in switch_dict:
            new_task.__set_bind(switch_dict['bind'])
        if 'output' in switch_dict:
            new_task.__set_output(switch_dict['output'])
        return new_task
