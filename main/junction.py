'''
Created on 2015-7-19

@author: ZL
'''
import os
import shutil
import subprocess
import configparser
import sys
import tempfile

# 配置文件名名称
CONFIG_FILE_NAME = 'config.ini'

CONFIG_SECION_NAME = 'config'

PATH_ALIAS_SECION_NAME = 'pathAlias'

CONFIG = {
# 原始文件夹重命名备份
'renameOriginFolder' : True,

# 原始文件夹重命名后缀
'renameFolderSubfix' : '_bak',

# 清空原始文件夹,只有当  renameOriginFolder 为 True 时该配置才会生效
'clearOriginFolder' : False,

# 当目录文件夹无效时，跳过
'skipInvalidTarget':False,

# 源文件从根目录开始最小深度要求
'minDirDeepth':2
}

#文件夹别名
PATH_ALIAS = {
    'UserHome':os.path.expanduser("~"),
    'Temp':tempfile.gettempdir()   
}


def loadConfig():
    currDir = os.path.dirname(os.path.abspath(__file__))
    configFilePath = currDir + os.path.sep + CONFIG_FILE_NAME;
    config = configparser.ConfigParser()
    config.read(configFilePath, "UTF-8")
    parsePathAlias(PATH_ALIAS, config[PATH_ALIAS_SECION_NAME])
    parseConfigSection(CONFIG, config[CONFIG_SECION_NAME])
    #重新构造 变量替换
    return parseTargetSection(config);
#     sections = list(filter(lambda s: s.startswith(CONFIG_SECION_NAME) == False, config.sections()))

def parseTargetSection(old):
    new = configparser.RawConfigParser()
    sections=old.sections()
    for skey in sections:
        newSkeyName=dictStrFormat(skey,PATH_ALIAS)
        new.add_section(newSkeyName)
        for key in old[skey]:
            new.set(newSkeyName, key, dictStrFormat(old[skey][key],PATH_ALIAS))                
    return new;

def parseConfigSection(dictMap, section):
    for key in dictMap:        
        varType = type(dictMap[key])
        if(key not in section):
            continue
        if(varType == bool):
            dictMap[key] = section[key] in ['true', 'True']
        else:
            dictMap[key] = (varType)(section[key])

def parsePathAlias(dictMap, section):
    for key in section: 
        dictMap[key] = dictStrFormat(section[key],dictMap)
                        
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
    ret = subprocess.Popen(["junction", path, target], stdout=subprocess.PIPE)
    ret.wait()
    if(ret.returncode != 0):
        out = ret.stdout
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
    if(os.path.isdir(path) == False):
        print(path + " is not a fonder!")
        return False;
    try:
        shutil.rmtree(path)
        return True
    except Exception as err:
        print(err)
        return False

def clearDirectory(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        if(os.path.isfile(file_path)):
            os.unlink(file_path)
        elif(os.path.isdir(file_path)):
            shutil.rmtree(file_path)
            

def varStrFormat(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))

def dictStrFormat(text, dictMap):
    return text.format_map(safesub(dictMap))
            
class safesub(dict):
    """防止key找不到"""
    def __missing__(self, key):
        return '{' + key + '}'

