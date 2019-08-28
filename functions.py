# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 11:32:06 2019

@author: zheng
"""

def my_function(a, b=None):
    if b is None:
        print("b is None, returning a")
        return a
    else:
        print("b is not None, returning a + b")
        return a + b

if __name__ == "__main__":
    c = my_function(a=5, b=None)
    print("value of c is", c)
    d = my_function(a=5, b=4)
    print("value of d is", d)