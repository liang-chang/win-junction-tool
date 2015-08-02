# coding=utf-8
import junction
import os

 
FILE_CONFIGS = junction.loadConfig()

#删去 配置项  config section
FILE_CONFIGS.remove_section(junction.CONFIG_SECION_NAME)

CONFIG = junction.CONFIG

successCount=0;       
failCount=0;
sections=FILE_CONFIGS
for target in sections:
    if(os.path.isdir(target) == False):
        print("dir: " + target + " is invalid!")
        continue
    print("\n")
    print("Target:" + os.path.realpath(target))
    part = FILE_CONFIGS[target]
    for key in part:        
        path = part[key]
        
        # 处理路径最后面出现路径分隔符的问题
        path = os.path.realpath(path)
         
        # 创建文件夹备份文件    
        if(CONFIG['renameOriginFolder']==True and not os.path.exists(path + CONFIG['renameFolderSubfix'])):
            os.makedirs(path + CONFIG['renameFolderSubfix'])
         
        # 删除源文件夹
        if(os.path.exists(path) == True):
            # 是否已经指向指定文件夹
            if(junction.isFolderJunctionTo(path, os.path.realpath(target)) == True):
                print(path + " has linked to target , skip ")
                continue
             
            # 源文件夹深度判断， 避免删除 根目录
            if(CONFIG['clearOriginFolder']==True and junction.getFolderDeepth(path) >= 2):
                if(junction.isJunction(path)==True):
                    #是符号链接
                    if(junction.delJunction(path)==True):
                        successCount+=1
                    else:
                        failCount+=1;
                else:
                    #普通文件夹 
                    if(junction.delDir(path)==True):
                        successCount+=1
                    else:
                        failCount+=1;
                 
        #创建 junction 
        ret = junction.createJunction(path, target)
        if(ret==True):
            print(path+" create success!")
        else:
            print(path+" create failed!")
#         
# # http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output        
# https://docs.python.org/3/library/subprocess.html