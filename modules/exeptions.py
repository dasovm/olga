class DestinationException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value == 'NotFound':
            return repr('Select a destination before try to download. Value = ' + self.value)
        if self.value == 'Invalid':
            return repr('You entered a invalid path. Value = ' + self.value)
        else:
            return repr('You did everything right, yet here you are. Value = ' + self.value)


class FileNameException(Exception):
    pass
