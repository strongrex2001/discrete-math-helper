# -*- coding: utf-8 -*-
"""
Tokenize string input.
Created on Wed Sep 18 13:18:07 2019

@author: eliphat
"""
import collections
import lcommons as commons


whitespaces = {' ', '\t', '\r', '\n'}
end_tokens = collections.defaultdict(list)
for op in commons.ops:
    end_tokens[op[0]].append(op)
for op in commons.spec:
    end_tokens[op[0]].append(op)


def put_word(tokens, string):
    if len(string) > 0:
        if string in commons.keywords:
            tokens.append(('keyword', string))
        elif string in commons.ops:
            tokens.append(('op', string))
        elif string in commons.spec:
            tokens.append(('special', string))
        else:
            tokens.append(('token', string))


def put_chlist(tokens, chlist):
    put_word(tokens, ''.join(chlist))
    chlist.clear()


def tokenize(s):
    tokens = []
    p = []
    i = 0
    while i < len(s):
        ch = s[i]
        i += 1
        if ch in whitespaces:
            put_chlist(tokens, p)
        elif ch in end_tokens:
            put_chlist(tokens, p)
            possibilities = end_tokens[ch]
            ac = False
            for end_tk in possibilities:
                if len(end_tk) == 1 or s[i - 1: i - 1 + len(end_tk)] == end_tk:
                    ac = True
                    put_word(tokens, end_tk)
                    i = i - 1 + len(end_tk)
            if not ac:
                raise Exception("Requires " + str(possibilities)
                                + "at '%s'" % ch)
        else:
            p.append(ch)
    if p:
        put_chlist(tokens, p)
    put_word(tokens, '&EOF')
    return tokens
