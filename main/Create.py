# coding=utf-8
import junction
import os
import shutil 

FILE_CONFIGS = junction.loadConfig()
# 删去 配置项  config section
FILE_CONFIGS.remove_section(junction.CONFIG_SECION_NAME)
FILE_CONFIGS.remove_section(junction.PATH_ALIAS_SECION_NAME)

CONFIG = junction.CONFIG
PATH_ALIAS = junction.PATH_ALIAS;

report = {
'totalCount' : 0,
'successCount' : 0,
'failCount' : 0,
'sectionCount' : 0,
'rename':0,
'renameSkip':0,
'skipInvalidSource':0
}

print("Create start ……")

print(CONFIG)

sections = FILE_CONFIGS.sections()

sectionIndex = 0;

processBreak = False

report['sectionCount'] = len(sections);

for target in sections:
    sectionIndex += 1
    print()
        
    print("Target index:" + str(sectionIndex))
            
    section = FILE_CONFIGS[target]
    
    target = os.path.realpath(target)
    
    size = len(section)
    report['totalCount'] += size;
        
    if(os.path.isdir(target) == False):
        print("dir: " + target + " is invalid!")
        if(CONFIG['skipInvalidTarget'] == True):
            print('{size} create junction Failed !!'.format(size=size))
            report['failCount'] += size
            continue
        else:
            print('\nTarget dir :\n {target} \nis not directory or not exist !'.format(target=target))
            print('\nCreate terminated!')
            processBreak = True
            break
    print("Target:" + target)
    
    for key in section:        
        path = section[key]
                
        # 处理路径最后面出现路径分隔符的问题
        path = os.path.realpath(path)
        
        # 创建文件夹备份文件
        if(CONFIG['renameOriginFolder'] == True and os.path.exists(path)):
            rename = path + CONFIG['renameFolderSubfix']
            if(os.path.exists(rename)):
                print("{rename}  has existed , skip rename".format(rename=rename))
                report['renameSkip'] += 1
            else:
                os.rename(path, rename)
                report['rename'] += 1
                # 源文件夹深度判断， 避免删除 根目录
                if(CONFIG['clearOriginFolder'] == True and junction.getFolderDeepth(rename) >= CONFIG['minDirDeepth']):                
                    junction.clearDirectory(rename)
        # 不需要备份时，删除源文件夹
        if(os.path.exists(path)):
            result, d = junction.isJunction(path)
            if(result == True):
                junction.delJunction(path)
            else:
                shutil.rmtree(path, True)
        
        if(CONFIG['skipNoParentSource'] == False):
            par = os.path.abspath(os.path.join(path, os.pardir))        
            if(os.path.exists(par) == False):
                report['skipInvalidSource'] += 1                
                continue
            
        # 创建 junction 
        ret = junction.createJunction(path, target)
        if(ret == True):
            report['successCount'] += 1
            print(path + " create junction success!")
        else:
            report['failCount'] += 1
            print(path + " create junction failed!")
print()
print("Create result :")
if(processBreak == False):
    print('Section:{sectionCount}'.format_map(report))
    print('Total:{totalCount}, Success:{successCount}, Fail:{failCount},Rename:{rename},Rename skip:{renameSkip}'.format_map(report))
else:
    print('create failed,please check log!')
# # http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output        
# https://docs.python.org/3/library/subprocess.html
