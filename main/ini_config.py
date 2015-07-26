# coding=utf-8
import junction

 
sections = junction.loadConfig()
for key in sections:
    print(key)
config=junction.CONFIG

# 
# sections = list(filter(lambda s: s.startswith("config") == False, config.sections()))
# 
# successCount=0;       
# failCount=0;
# for target in sections:
#     if(os.path.isdir(target) == False):
#         print("dir: " + target + " is invalid!")
#         continue
#     print("\n")
#     print("Target:" + os.path.realpath(target))
#     part = config[target]    
#     for key in part:        
#         path = part[key]
#         # 处理路径最后面出现路径分隔符的问题
#         path = os.path.realpath(path)
#         
#         # 创建文件夹备份文件    
#         if(CONFIG['renameOriginFolder']==True and not os.path.exists(path + CONFIG['renameFolderSubfix'])):
#             os.makedirs(path + CONFIG['renameFolderSubfix'])
#         
#         # 删除源文件夹
#         if(os.path.exists(path) == True):
#             # 是否已经指向指定文件夹
#             if(isFolderJunctionTo(path, os.path.realpath(target)) == True):
#                 print(path + " has linked to target , skip ")
#                 continue
#             
#             # 源文件夹深度判断， 避免删除 根目录
#             if(CONFIG['clearOriginFolder']==True and getFolderDeepth(path) >= 2):
#                 if(isJunction(path)==True):
#                     #是符号链接
#                     if(delJunction(path)==True):
#                         successCount+=1
#                     else:
#                         failCount+=1;
#                 else:
#                     #普通文件夹 
#                     if(delDir(path)==True):
#                         successCount+=1
#                     else:
#                         failCount+=1;
#                 
#         #创建 junction 
#         ret = createJunction(path, target)
#         if(ret==True):
#             print(path+" create success!")
#         else:
#             print(path+" create failed!")
# #         if(os.path.isdir(path) == True): 
#         
# # http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output        
# # https://docs.python.org/3/library/subprocess.html
