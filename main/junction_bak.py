'''
Created on 2015-7-19

@author: ZL
'''
import os
import shutil
import configparser
import shlex
import subprocess

# 配置文件名名称
CONFIG_FILE_NAME = 'config.ini'

CONFIG = {
# 原始文件夹重命名备份
'renameOriginFolder' : True,

# 原始文件夹重命名后缀
'renameFolderSubfix' : '_bak',

# 清空原始文件夹
'clearOriginFolder' : True,

# 创建 junction 文件夹时
'createParentDirectory':True,

# 源文件从根目录开始最小深度要求
'minDirDeepth':2
}

class Junction(object):
    def __init__(self,selfparams):
        pass
    
    @staticmethod
    def getFolderDeepth(self,path):
        path = os.path.abspath(path).lower();                         
        parentDir = os.path.abspath(os.path.join(path, os.pardir)).lower()
        lastDir = path
        deepth = 0;    
        while parentDir != lastDir:
            deepth += 1
            lastDir = parentDir;
            parentDir = os.path.abspath(os.path.join(parentDir, os.pardir)).lower()
        return deepth
    

    @staticmethod
    def isFolderJunctionTo(self,source, target):
        path = os.path.abspath(source)
        output = os.popen('junction ' + path)
        out = output.readlines();
        size = len(out)
        # 如果是 junction 点的话，返回 9行
        # 否则是 7 行
        if(size < 8):
            return False
        parseTarget = os.path.abspath(out[6].strip()[17:].strip().lower())
        target = os.path.abspath(target).lower();    
        return parseTarget == target

    @staticmethod    
    def createJunction(self,source, target):
        path = os.path.abspath(source)
        ret=subprocess.Popen(["junction", path,target],stdout=subprocess.PIPE)
        ret.wait()
        if(ret.returncode != 0):
            out=ret.stdout
            print(out)
        # 创建成功 返回 0
        # 否则 返回  非零
        return ret.returncode == 0
    

    def isJunction(self,source):
        path = os.path.abspath(source)
        output = os.popen('junction ' + path)
        out = output.readlines();    
        size = len(out)    
        # 如果是 junction 点的话，返回 9行
        # 否则是 7 行
        return size > 8
    
    @staticmethod
    def delJunction(self,source):     
        path = os.path.abspath(source)
        output = os.popen('junction -d ' + path)
        out = output.readlines();
        # 错误8行
        # 正确6行    
        return len(out) < 8
    
    @staticmethod
    def delDir(self,path):
        path = os.path.abspath(path)
        if(os.path.isdir(path)==False):
            print(path+" is not a fonder!")
            return False;
        try:
            shutil.rmtree(path)
            return True
        except Exception as err:
            print(err)
            return False
