# -*- coding: utf-8 -*-
# copyright@mathu
# Author: Ruimin Wang, ruimin.wang13@gmail.com
# Func: define all exceptions

class ParserException(Exception):
    def __init__(self, value):
        self.value = "ParserException: {}".format(value)
    def __str__(self):
        return repr(self.value)

class LoaderException(Exception):
    def __init__(self, value):
        self.value = "LoaderException: {}".format(value)
    def __str__(self):
        return repr(self.value)

class TimeoutException(Exception):
    def __init__(self, value):
        self.value = "TimeoutException: {}".format(value)
    def __str__(self):
        return repr(self.value)


class GeneratorException(Exception):
    def __init__(self, value):
        self.value = "GeneratorException: {}".format(value)
    def __str__(self):
        return repr(self.value)

