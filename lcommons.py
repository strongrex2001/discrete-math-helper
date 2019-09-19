# -*- coding: utf-8 -*-
"""
Common definitions used by other modules.
Created on Wed Sep 18 13:30:42 2019

@author: eliphat
"""


builtin_fns = {'truth_table', 'always_holds'}
keywords = builtin_fns.union({'var', '&EOF'})
ops = {
    '&': 2, '|': 3, '~': 1, '->': 4, '<->': 5, '^': 6
}
spec = {
    '(', ')', ',', ';'
}
bop_table = {
    '^': lambda x, y: x ^ y,
    '&': lambda x, y: x and y,
    '|': lambda x, y: x or y,
    '->': lambda x, y: False if x and not y else True,
    '<->': lambda x, y: x == y
}
sop_table = {
    '~': lambda x: not x
}
