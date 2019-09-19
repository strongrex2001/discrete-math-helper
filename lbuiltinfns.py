# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 19:38:15 2019

@author: eliphat
"""
import levaluator


def builtin_fn_truth_table(env, data):
    numeval_expr = levaluator.numeval_expr
    print('\t'.join(env + ['result']))
    for i in range(2 ** len(env)):
        numenv = {env[bit]: (i & (1 << bit)) > 0 for bit in range(len(env))}
        for bit in range(len(env)):
            print('T' if numenv[env[bit]] else 'F', end='\t')
        print('T' if numeval_expr(numenv, data) else 'F')


def builtin_fn_always_holds(env, data):
    numeval_expr = levaluator.numeval_expr
    print('T' if all(
        numeval_expr(
            {env[bit]: (i & (1 << bit)) > 0 for bit in range(len(env))},
            data
        ) for i in range(2 ** len(env))
    ) else 'F')
