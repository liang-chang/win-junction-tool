'''
Created on 2013-9-14

@author: ZL
'''
import os
import json
import shutil

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
'createParentDirectory':False
}


def loadConfig():
    currDir = os.path.dirname(os.path.abspath(__file__))

    configFilePath=currDir + os.path.sep + CONFIG_FILE_NAME;
    if(os.path.isfile(configFilePath)==False):
        print("no config file :"+configFilePath)
        exit(0)
    with open(configFilePath, 'r') as f:
        config = json.load(f)       
    return config


def getFolderDeepth(path):
    path=os.path.abspath(path).lower();                         
    parentDir = os.path.abspath(os.path.join(path, os.pardir)).lower()
    lastDir=path
    deepth=0;    
    while parentDir!=lastDir:
        deepth+=1
        lastDir=parentDir;
        parentDir = os.path.abspath(os.path.join(path, os.pardir)).lower()
    return deepth
#=================================================================

def isFolderJunctionTo(source, target):
    path = os.path.abspath(source)
    output = os.popen('junction ' + path)
    out = output.readlines();
    size = len(out)
    print(size)
    # 如果是 junction 点的话，返回 9行
    # 否则是 8行
    if(size < 8):
        return False
    parseTarget = os.path.abspath(out[6].strip()[17:].strip().lower())
    target = os.path.abspath(target).lower();    
    return parseTarget == target
#=================================================================


config=loadConfig()
# CONFIGkey in config:
#     if(os.paCONFIGir(key)==False):
#         print("dir is invalid!")
#         continue
#     for value in config[key]:        # CONFIG   #处理路径最后面出现路径分隔符的问题
#         value=os.path.realpath(value)
#         
#         if not os.path.exists(value+ORIGIN_FOLDER_SUBFIX):
#             os.makedirs(value+ORIGIN_FOLDER_SUBFIX)
#         if(os.path.isdir(value)==True):                        
#             if(getFolderDeepth(value) > 2 ):
#                 #源文件夹深度判断， 避免删除 根目录
#                 shutil.rmtree(value)
#             
#         
#         
#         

        