'''
Created on 2015-7-19

@author: ZL
'''
#import shlex
#import configparser
import os
import shutil
import subprocess
import configparser

# 配置文件名名称
CONFIG_FILE_NAME = 'config.ini'

CONFIG_SECION_NAME='config'

CONFIG = {
# 原始文件夹重命名备份
'renameOriginFolder' : True,

# 原始文件夹重命名后缀
'renameFolderSubfix' : '_bak',

# 清空原始文件夹
'clearOriginFolder' : True,

#当目录文件夹无效时，跳过
'skipInvalidTarget':False,

# 源文件从根目录开始最小深度要求
'minDirDeepth':2
}

def loadConfig():
    currDir = os.path.dirname(os.path.abspath(__file__))
    configFilePath=currDir + os.path.sep + CONFIG_FILE_NAME;
    config = configparser.ConfigParser()
    config.read(configFilePath,"UTF-8")
    secion=config[CONFIG_SECION_NAME]    
    for key in CONFIG: 
        varType=type(CONFIG[key])
        if(key not in secion):
            continue
        if(varType==bool):
            CONFIG[key]=secion[key] in ['true', 'True']
        else:
            CONFIG[key]=(varType)(secion[key])
#     config.remove_option(CONFIG_SECION_NAME)
#     sections = list(filter(lambda s: s.startswith(CONFIG_SECION_NAME) == False, config.sections()))
    return config
            
def getFolderDeepth(path):
    path = os.path.abspath(path).lower();                         
    parentDir = os.path.abspath(os.path.join(path, os.pardir)).lower()
    lastDir = path
    deepth = 0;    
    while parentDir != lastDir:
        deepth += 1
        lastDir = parentDir;
        parentDir = os.path.abspath(os.path.join(parentDir, os.pardir)).lower()
    return deepth


def isFolderJunctionTo(source, target):
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

   
def createJunction(source, target):
    path = os.path.abspath(source)
    ret=subprocess.Popen(["junction", path,target],stdout=subprocess.PIPE)
    ret.wait()
    if(ret.returncode != 0):
        out=ret.stdout
        print(out)
    # 创建成功 返回 0
    # 否则 返回  非零
    return ret.returncode == 0


def isJunction(source):
    path = os.path.abspath(source)
    output = os.popen('junction ' + path)
    out = output.readlines();    
    size = len(out)    
    # 如果是 junction 点的话，返回 9行
    # 否则是 7 行
    return size > 8


def delJunction(source):     
    path = os.path.abspath(source)
    output = os.popen('junction -d ' + path)
    out = output.readlines();
    # 错误8行
    # 正确6行    
    return len(out) < 8

def delDir(path):
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
