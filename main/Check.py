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

print("Check start ……")

sections = FILE_CONFIGS.sections()

sectionIndex = 0;
report['sectionCount']=len(sections);

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
        
        if(junction.isFolderJunctionTo(path, target) == True):
            report['rightCount'] += 1     
        else:
            report['wrongCount'] += 1
            print('{path} wrong junction target'.format(path=path))           
        
print()
print("Check result :")
print('Section:{sectionCount}'.format_map(report))
print('Total:{totalCount}, Right:{rightCount}, Wrong:{wrongCount}'.format_map(report))
# # http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output        
# https://docs.python.org/3/library/subprocess.html
