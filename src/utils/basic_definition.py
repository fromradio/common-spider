# -*- coding: utf-8 -*-
# Author: Ruimin Wang, ruimin.wang13@gmail.com
# Func the very basic definitions




FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'


def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider

