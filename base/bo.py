__author__ = 'benjamin kim'

"""
Base Objects
"""


class BaseObject:
    def __init__(self):
        return


class BoException(Exception):
    msg = ""
    value = None
    def __init__(self, message_, value_=None):
        self.msg = message_
        self.value = value_

    def __str__(self):
        return "MSG: {}, VALUE: {}".format(repr(self.msg), repr(self.value))
