# -*- coding: utf-8 -*-

import numpy as np
from inspect import signature
import sys
from graphviz import *


class Node(object):
    '''The node object.

    Node objects can be divided into 2 types:
    1. Internal Node
        Internal nodes have a parameter 'index' which indicates the depth of nodes.
    2. Leaf Node
        Leaf nodes have a parameter 'value'.
    '''
    id = None

    def __init__(self, index=None, value=None, left=None, right=None):
        if index != None and value != None:
            raise ValueError('The index and value parameters must not be passed at the same time.')
        self.index = index
        self.value = value
        self.left = left
        self.right = right

    def is_internal(self):
        return self.index != None

    def is_leaf(self):
        return (self.index == None) and (self.value != None)

    def __repr__(self):
        if self.is_internal():
            return '<Internal Node index={}>'.format(self.index)
        elif self.is_leaf():
            return '<Leaf value={}>'.format(self.value)
        return '<Unknown Node>'


class BDD(object):
    '''Binary Dicision Digram (BDD)

    A BDD object represents a Boolean function, returning either 1 or 0 from a given Boolean variables.

    Attributes
    ----------
    root : Node object
        The root node of the BDD.
    '''

    def __init__(self, func):
        def n_parameters(func):
            '''Get the number of parameters of a function.

            Parameters
            ----------
            func : function
                A function object.

            Returns
            -------
            int
                The length of paramters.
            '''
            return len(signature(func).parameters)

        def build_tree(path, func):
            if len(path) == self.nbvar:
                leaf = Node(value=func(*path))
                return leaf
            else:
                node = Node(index=len(path))
                node.left = build_tree(path + [0], func)
                node.right = build_tree(path + [1], func)
                return node

        self.nbvar = n_parameters(func)
        self.root = build_tree([], func)

    def traverse(self):
        def _traverse(node, levels):
            if node.is_internal():
                levels[node.index].append(node)
                _traverse(node.left, levels)
                _traverse(node.right, levels)
            elif node.is_leaf():
                levels[len(levels) - 1].append(node)

        levels = []
        for i in range(self.nbvar + 1):
            levels.append([])
        _traverse(self.root, levels)
        return levels


def t(a, b, c):
    return a and b or c


bdd = BDD(t)
bdd.root.left.left.id

bdd.traverse()
