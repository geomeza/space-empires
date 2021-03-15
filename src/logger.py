import os
import difflib
import filecmp

class Logger:

    def __init__(self, file_name):
        self.file_name = file_name
        self.logging_file = self.make_logging_file()

    def make_logging_file(self):
        return open(os.path.join('logs', self.file_name), 'a+')

    def log(self, string):
        if string == '\n':
            self.logging_file.write(string)
            return
        self.logging_file.write(string + '\n')

    def close_file(self):
        self.logging_file.close()
