# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 18:23:24 2019

@author: zheng
"""

class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def run(self, speed):
        print("I am running at", speed, "and my name is", self.name)
        
    def get_older(self):
        print("Happy Birthday", self.name)
        self.age += 1
        
        
dog1 = Dog('Flash', 3)
dog2 = Dog('Speedy', 4)

dog1.run(speed='1m/s')
print(dog1.age)
dog1.get_older()
print(dog1.age)

