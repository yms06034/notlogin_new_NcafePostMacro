import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon

path = 'test.txt'
file = open(path, 'rt', encoding='UTF8')
contents = file.read()

print(contents)
print( '------------------')

print(contents.split(']')[0][1:])