# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 19:24:46 2019

@author: zheng
"""
import pandas as pd
def plus(x):
    return x + 1

f = lambda x: x+1

df = pd.DataFrame([[1,2], [2,3],[3,4]], columns=['a', 'b'])
df['c']=['copyright', '1', '2']
# get the critieria the easy way by applying to the whole series
greater_than_two=df['a']>=2
# .apply to apply a function on each element within the series
is_digit = df['c'].apply(lambda x : x.isdigit())
df_greater_than_two = df[greater_than_two]
df_is_digit = df[is_digit]

# another way to do this without lambda function
def is_digit_func(x):
    return x.isdigit()

# is_digit_func is passed to apply as an argument, so we don't call it here
is_digit2 = df['c'].apply(is_digit_func)
df_is_digit2 = df[is_digit2]

"""You can actually pass a function as an argument to another function.
For example: We define two functions multi and minus for calculating the 
multiplication and difference of a and b, respective. And we define a third
function called run to run those two functions.
"""
def multi(a, b):
    print("calculate a multiply b")
    return a*b

def minus(a, b):
    print("calculate a minus b")
    return a-b

def run(func, a, b):
    return func(a, b)
    
c = run(multi, 3, 4)  # see that we are passing the function multi to the function run here
d = run(minus, 3, 4)
