import yaml


class Task():
    def __init__(self, yml):
        with open(yml) as f:
            self.__yml = yaml.load(f, Loader=yaml.SafeLoader)

    def get_task(self):
        input_cmd = self.__yml['base_task']['input']
        input_cmd += ' | fzf'
        return input_cmd

