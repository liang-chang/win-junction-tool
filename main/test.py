'''
Created on 2015-7-19

@author: ZL
'''
import os
import shutil
import configparser
import sys
import tempfile
import ctypes


def isFolderJunctionTo(path, target):
    path = os.path.abspath(path)
    target = os.path.abspath(target)    
    output = os.popen(r'junction "{path}"'.format(path=path))
    out = output.readlines();
    
    filter(lambda s: s.startswith("") == False, out)
    
    # 如果是 junction 点的话，返回 9行
    # 否则是 7 行
#     if(size!=9):
#         return False
    parseTarget = os.path.abspath(out[6].strip()[17:].strip().lower())
    target = os.path.abspath(target).lower();    
    return parseTarget == target

def isJunction(path):
    path = os.path.abspath(path)
    output = os.popen(r'junction "{path}"'.format(path=path))
    out = output.readlines()
    #sections = list(filter(lambda s: s.startswith(CONFIG_SECION_NAME) == False, config.sections()))
    #sections = list(filter(lambda s: s.startswith(CONFIG_SECION_NAME) == False, config.sections()))

    print(out)
    size = len(out)
    # 如果是 junction 点的话，返回9行
    # 否则是 7 行    
    return size ==9

print(isJunction("v:/tt"))
