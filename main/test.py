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
    result, p = isJunction(path)
    if(result==True):
        p=os.path.abspath(p).lower()
        if(p==target):
            return True
    return False
 

def isJunction(path):
    path = os.path.abspath(path).replace("\\", "/")
    output = os.popen(r'junction "{path}"'.format(path=path)).readlines()
    pattern = re.compile(path + ':\s+?JUNCTION')
    outLen = len(output)
    nextStart = 0;
    for i in range(outLen):
        s = output[i].replace("\\", "/")
        ret = pattern.match(s)
        if(ret):
            nextStart = i + 1
            break    
    if(i + 1 == outLen):
        return (False, "")
    while nextStart <= outLen:
        s = output[nextStart].strip();
        nextStart+=1
        if(s.startswith("Substitute Name:") == True):
            s = s[len("Substitute Name:"):]
            break
    return (True, s.strip())

def createJunction(path, target):
    path = os.path.abspath(path)
    target=os.path.abspath(target)    
    output = os.popen(r'junction "{path}" "{target}"'.format(path=path,target=target))
    out = output.readlines()
    size = len(out)
    path=path.replace("\\", "/")
    pattern = re.compile("Created:\s+?"+path)
    for i in range(size):
        s = out[i].replace("\\", "/")
        ret = pattern.match(s)
        if(ret):
            return True
    return False

def delJunction(source):     
    path = os.path.abspath(source)    
    output = os.popen(r'junction -d "{path}"'.format(path=path))
    out = output.readlines()
    path=path.replace("\\", "/")
    pattern = re.compile("Deleted\s+?"+path)
    for s in out:
        s = s.replace("\\", "/")
        ret = pattern.match(s)
        if(ret):
            return True
    return False
    
#print(createJunction(r"v:\tt", r"v:\temp"))
#print(delJunction(r"v:\tt"))
path=r"V:\useless_temp\G\aaaaaaa";
print(os.pardir)
print(os.path.join(path, os.pardir))
print(os.path.abspath(os.path.join(path, os.pardir)))


# print(isJunction(r"C:\useless\A"))
# print(isFolderJunctionTo(r"v:\tt",r"v:\temp"))
                

