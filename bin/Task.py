from Opts import Opts
from Bind import Bind
from Output import Output
from Transform import Transform


class Task():
    def __init__(self, yml, variables, continue_expect):
        self.__yml = yml
        self.__variables = variables
        self.__set_input(yml['input'])
        self.__transform = Transform(yml.get('transform', ''), variables)
        self.__opts = Opts(yml.get('opts', []), variables)
        self.__query = yml.get('query', '')
        self.__preview = yml.get('preview', '')
        self.__bind = Bind(yml.get('bind', {}), variables)
        self.__output = Output(yml.get('output', {}), variables)
        self.__continue_expect = continue_expect

    def __get_input(self):
        return self.__variables.expand(self.__input)

    def __get_opts(self):
        return self.__opts.to_string()

    def __get_preview(self):
        if len(self.__preview) > 0:
            expanded = self.__variables.expand(self.__preview)
            return '--preview="{}"'.format(expanded)
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

    def __set_transform_opts(self):
        if len(self.__preview) == 0:
            self.__preview = 'echo {2..}'
        else:
            self.__preview = self.__preview.replace('{}', '{2..}')
        self.__opts.set_nth_for_transform()

    def __get_expect(self):
        expects = self.__continue_expect + self.__output.get_expect()
        if 'enter' not in expects:
            expects.append('enter')
        return '--expect="{}"'.format(','.join(expects))

    def __get_fzf_options(self):
        return '{} {} {} {} {}'.format(self.__get_opts(), self.__get_query(),
                                       self.__get_preview(), self.__get_bind(),
                                       self.__get_expect())

    def get_cmd(self):
        if self.__transform.exists():
            self.__set_transform_opts()
            cmd = '{} | tee {} | {} | cat -n | fzf {}'.format(
                self.__get_input(), Transform.get_temp_name(),
                self.__transform.get_cmd(), self.__get_fzf_options())
            return cmd
        else:
            cmd = '{} | fzf {}'.format(self.__get_input(),
                                       self.__get_fzf_options())
            return cmd

    def output(self, result):
        query = result.split('\n')[0]
        key = result.split('\n')[1]
        content = '\n'.join(result.split('\n')[2:])
        self.__output.write(query, key, content)

    def is_continue(self, result):
        key = result.split('\n')[1]
        return key in self.__continue_expect

    def create_continue_task(self, continue_dict):
        new_task = Task(self.__yml, self.__variables, self.__continue_expect)
        if 'input' in continue_dict:
            new_task.__set_input(continue_dict['input'])
        if 'transform' in continue_dict:
            new_task.__set_transform(continue_dict['transform'])
        if 'opts' in continue_dict:
            new_task.__set_opts(continue_dict['opts'])
        if 'query' in continue_dict:
            new_task.__set_query(continue_dict['query'])
        else:
            new_task.__set_query('{pre_query}')
        if 'preview' in continue_dict:
            new_task.__set_preview(continue_dict['preview'])
        if 'bind' in continue_dict:
            new_task.__set_bind(continue_dict['bind'])
        if 'output' in continue_dict:
            new_task.__set_output(continue_dict['output'])
        return new_task
