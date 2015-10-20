# coding=utf-8
import junction
import os

FILE_CONFIGS = junction.loadConfig()
# 删去 配置项  config section
FILE_CONFIGS.remove_section(junction.CONFIG_SECION_NAME)
FILE_CONFIGS.remove_section(junction.PATH_ALIAS_SECION_NAME)

CONFIG = junction.CONFIG
PATH_ALIAS = junction.PATH_ALIAS;

report = {
'totalCount' : 0,
'rightCount' : 0,
'wrongCount' : 0,
'sectionCount' : 0,
}

print("Recovery start ……")

sections = FILE_CONFIGS.sections()

sectionIndex = 0;
report['sectionCount'] = len(sections);

for target in sections:
    print()
        
    print("Target index:" + str(sectionIndex))
    sectionIndex += 1
            
    section = FILE_CONFIGS[target]
    
    target = os.path.realpath(target)
    
    size = len(section)
    report['totalCount'] += size;
        
    if(os.path.isdir(target) == False):
        print("dir: " + target + " is invalid!")
        report['wrongCount'] += size
        continue        
    print("Target:" + target)
    
    for key in section:        
        path = section[key]
                
        # 处理路径最后面出现路径分隔符的问题
        path = os.path.realpath(path)
        
        # 如果源文件夹不存在，则跳过不处理
        if(os.path.exists(path) == False):            
            continue

        # 如果源文件夹存在，则删除（一般时 junction ），普通文件夹则不用处理                    
        if(os.path.exists(path) == True):
            result, d = junction.isJunction(path)
            if(result == True):
                junction.delJunction(path)
            else:
                continue
        
        # 如果存在备份文件夹，则恢复
        backDirName = path + junction.CONFIG['renameFolderSubfix']
        if(os.path.exists(backDirName)):
            os.rename(backDirName, path)
            continue
        
        # 创建源文件夹
        os.makedirs(path, mode=0o777, exist_ok=True)
                
print()
print("Check result :")
print('Section:{sectionCount}'.format_map(report))
print('Total:{totalCount}, Right:{rightCount}, Wrong:{wrongCount}'.format_map(report))
# # http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output        
# https://docs.python.org/3/library/subprocess.html
