__author__ = 'mazheng'

import inspect

MAGIC_STRING = "test"
SEPARATOR = '_'


class AutoTest(object):

    def _get_methods(self):
        return inspect.getmembers(self, predicate=inspect.ismethod)

    @staticmethod
    def _is_valid(name):
        return name.startswith(MAGIC_STRING)

    @staticmethod
    def _get_order(name):
        pair = name.split(SEPARATOR)
        if len(pair) == 1:
            return 0
        else:
            return int(pair[1]) if pair[1].isdigit() else 0

    def run(self):
        valid_methods = []
        for method in self._get_methods():
            if self._is_valid(method[0]):
                order = self._get_order(method[0])
                valid_methods.insert(order, method)

        for vm in valid_methods:
            print 'run:', vm[0], vm[1].__doc__
            res = vm[1]()
            if res:
                print 'failed'
                break
            print 'success'
        return res
