# -*- coding: utf-8 -*-
"""
Created on Sun May 17 16:57:24 2015

@author: Martin Nguyen
"""

class node(object):
    def __init__(self,value, left = None,right = None):
        self.value = value
        self.left = left
        self.right = right