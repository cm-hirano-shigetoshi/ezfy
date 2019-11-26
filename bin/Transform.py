import tempfile

temp_file = None


class Transform():
    def __init__(self, transform, variables):
        self.__transform = ""
        self.__variables = variables
        self.set(transform)

    def exists(self):
        return len(self.__transform) > 0

    def get_cmd(self):
        command = self.__variables.expand(self.__transform)
        return command

    def set(self, transform):
        self.__transform = transform

    def get_temp_name():
        global temp_file
        if temp_file is None:
            temp_file = tempfile.NamedTemporaryFile()
        return temp_file.name

    def close_temp_file():
        global temp_file
        if temp_file is not None:
            temp_file.close()
            temp_file = None

    def adjust_preview(preview):
        cmd = 'cat {}'.format(Transform.get_temp_name())
        cmd += ' | {tooldir}/bin/line_selector.pl {1}'
        return preview.replace('{}', '$({})'.format(cmd))
