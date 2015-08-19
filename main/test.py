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
import re


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
    path=path.replace("\\", "/")
    output = os.popen(r'junction "{path}"'.format(path=path))
    out = output.readlines()
    #sections = list(filter(lambda s: s.startswith(CONFIG_SECION_NAME) == False, config.sections()))
    pattern = re.compile(path+':\s+?(\w+)')
    #sections = list(filter(lambda s: s.startswith(CONFIG_SECION_NAME) == False, config.sections()))
    find=False
    for s in out:
        print(s)
        s=s.replace("\\", "/")
        ret=pattern.match(s)
        if(ret):
            if(ret.group(1)=="JUNCTION"):
                pattern = re.compile("Substitute\s+?Name:\s+\(\w+)")
#         result = re.match(, s)
    
    return False,""
    # 如果是 junction 点的话，返回9行
    # 否则是 7 行    

print(isJunction("v:/tt"))
                

