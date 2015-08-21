'''
Created on 2015-7-19

@author: ZL
'''
import os
import shutil
import configparser
import sys
import tempfile
import re

# 配置文件名名称
CONFIG_FILE_NAME = 'config.ini'

CONFIG_SECION_NAME = 'config'

PATH_ALIAS_SECION_NAME = 'pathAlias'

CONFIG = {
# 原始文件夹重命名备份
'renameOriginFolder' : True,

# 原始文件夹重命名后缀
'renameFolderSubfix' : '_link_bak',

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


def isFolderJunctionTo(path, target):
    path = os.path.abspath(path)
    target = os.path.abspath(target).lower()    
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
    