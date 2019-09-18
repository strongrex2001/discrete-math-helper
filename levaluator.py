# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:12:36 2019

@author: eliphat
"""
import lcommons as commons


def numeval_token(numenv, expr):
    if expr[1] not in numenv:
        raise Exception("Variable Not Declared: " + str(expr[1]))
    return numenv[expr[1]]


def numeval_binexpr(numenv, expr):
    _, op, operand1, operand2 = expr
    return commons.bop_table[op](
               numeval_expr(numenv, operand1),
               numeval_expr(numenv, operand2)
           )


def numeval_unaryexpr(numenv, expr):
    _, op, operand = expr
    return commons.sop_table[op](numeval_expr(numenv, operand))


def numeval_expr(numenv, expr):
    drive_table = {
        'token': numeval_token,
        'uny_expr': numeval_unaryexpr,
        'bin_expr': numeval_binexpr
    }
    if expr[0] not in drive_table:
        raise Exception("Unrecognized Expression Type: " + str(expr[0]))
    return drive_table[expr[0]](numenv, expr)


def eval_expr(env, data):
    print('\t'.join(env + ['result']))
    for i in range(2 ** len(env)):
        numenv = {env[bit]: (i & (1 << bit)) > 0 for bit in range(len(env))}
        for bit in range(len(env)):
            print('T' if numenv[env[bit]] else 'F', end='\t')
        print('T' if numeval_expr(numenv, data) else 'F')


def eval_vars(env, data):
    if len(set(env) & set(data)) > 0:
        raise Exception("Variable(s) %s Declared Twice"
                        % str(set(env) & set(data)))
    env += data


def evaluate(statements, env=None):
    env = env or list()
    func_table = {
        'var_decl': eval_vars,
        'expr': eval_expr
    }
    for stype, data in statements:
        if stype not in func_table:
            raise Exception("Unrecognized AST Statement Type: " + str(stype))
        func_table[stype](env, data)
