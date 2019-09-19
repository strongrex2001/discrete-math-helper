# -*- coding: utf-8 -*-
"""
Parsing token sequence to AST.
Created on Wed Sep 18 13:54:35 2019

@author: eliphat
"""
import lcommons as commons


bops = sorted(commons.bop_table, key=lambda x: commons.ops[x])


def parse(tokens):
    data = [0]

    def lookahead():
        return tokens[data[0]]

    def next_token():
        data[0] += 1
        return lookahead()

    def match(token, error):
        if lookahead()[1] != token:
            raise Exception(error)
        next_token()

    def expr(order):
        if order < 0:
            return expr_atom()
        operand = expr(order - 1)
        if lookahead()[1] == bops[order]:
            next_token()
            return ('bin_expr', bops[order], operand, expr(order))
        return operand

    def expr_atom():
        if lookahead()[1] == '(':
            next_token()
            operand = expr(len(bops) - 1)
            match(')', "No Matching ')' Found for '('")
            return operand
        if lookahead()[0] == 'token':
            operand = lookahead()
            next_token()
            return operand
        if lookahead()[0] == 'op':
            if lookahead()[1] in commons.sop_table:
                op1 = lookahead()[1]
                next_token()
                return ('uny_expr', op1, expr(len(bops) - 1))
        raise Exception("Bad Token Met: " + str(lookahead()))

    def var_list():
        v1 = lookahead()
        if v1[0] != 'token':
            raise Exception("Non-token in Variable Declaration: " + str(v1))
        x = next_token()
        if x[1] == ',':
            next_token()
            return [v1[1], *var_list()]
        if x[1] == ';':
            next_token()
            return [v1[1]]
        raise Exception("',' or ';' Excepted after '" + v1[1] + "'")

    def statement():
        if lookahead()[1] == 'var':
            next_token()
            return ('var_decl', var_list())
        if lookahead()[0] == 'keyword':
            if lookahead()[1] in commons.builtin_fns:
                fn = lookahead()[1]
                next_token()
                match('(', 'Argument List Required after ' + fn)
                args = [expr(len(bops) - 1)]
                while lookahead()[1] == ',':
                    match(',', '')
                    args.append(expr(len(bops) - 1))
                match(')', "No Matching ')' Found for '('")
                match(';', "Missing ';'")
                return ('fn_run', (fn, args))
        if lookahead()[0] in ('token', 'op', 'special'):
            ret = ('expr', expr(len(bops) - 1))
            match(';', "Missing ';'")
            return ret
        raise Exception("Bad Token Met: " + str(lookahead()))

    statements = []
    while lookahead()[1] != '&EOF':
        statements.append(statement())
    return statements
