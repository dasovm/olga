def get_symbol_list():
    return import_text_file_to_string('./symbol_list.txt')


def import_text_file_to_string(path):
    file = open(path, 'r')
    return file.read()
