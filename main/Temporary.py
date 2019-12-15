import tempfile

temp_paths = {}


class Temporary():
    def create_temp_file(name):
        temp_paths[name] = tempfile.NamedTemporaryFile()

    def temp_path(name):
        return temp_paths[name].name
