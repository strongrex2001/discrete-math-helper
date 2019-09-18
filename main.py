# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 19:39:52 2019

@author: eliphat
"""
import sys
import io
import ltokenizer
import lparser
import levaluator


def main():
    inp = ''
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fi:
            inp = fi.read(-1)
    else:
        with io.StringIO() as buffer:
            line = ''
            while line != 'GO!':
                buffer.write(line)
                line = input()
            inp = buffer.getvalue()
    levaluator.evaluate(lparser.parse(ltokenizer.tokenize(inp)))


if __name__ == "__main__":
    main()
