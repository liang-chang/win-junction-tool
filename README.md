# win-junction-tool
batch create ntfs junction

批量创建 junction 的工具

一些软件比如 QQ , 开发用的IDE会大量的往硬盘写些文件，而这些文件通常是无用的日志文件类，大量的io还会拖慢系统。 一个比较好的解决方法是，创建 ramdisk 并把这些文件夹定向到ramdisk 上，利用 ramdisk 的高速及重启还原的特性，使这些无用的文件对系统的影响降到最小，同时也避免过多写入垃圾文件，减小清理。 那个文件夹重定向的功能就是 windows ntfs junction ，类似linux 上的软链接。

## 运行方法：
双击 Create.bat 、 Check.bat 、 Recovery.bat 等。
Create.bat 创建 junction 文件夹，是按配置文件创建 junction 文件 
Check.bat  检查，按 配置文件夹，检查源文件夹和目录文件夹是否正常
Recovery.bat  恢复

## 运行环境要求：
系统：windows xp/vista/7 (win 8/10 没有试验) <br/>
需要的环境：python 3<br/>

## Q&A <br/>
1.为什么要用 python3 做为运行环境？ <br/>
因为之前我在学python3，为了熟悉python3，所以我选用了python3作为运行环境。<br/>


## 配置文件 config.ini 介绍：<br/>

[config] <br/>
; 原始文件夹是否重命名备份，重命令名的规则添加 _link_bak 后缀 <br/>
renameOriginFolder = true<br/>

; 是否清空原始文件夹 <br/>
clearOriginFolder = false<br/>

;当目录文件夹无效时是否跳过，当target文件夹无效时，false 会终止运行；否则跳过 <br/>
skipInvalidTarget = false<br/>

;当源文件夹不存在，且父文件夹不存在时是否还要创建；false 不创建；true 会继续创建 <br/>
createSourceParent=false<br/>

;pathAlias 是给一些反复使用的文件夹起别名，<br/>
;内置了两个别名， UserHome 和 Temp ，分别指向用户目录和系统临时文件夹<br/>
;引用该文件夹别名时，只需要把名称用大括号包起来
;比如引用 Temp 该这样使用： {Temp} <br/>
[pathAlias] <br/>
;useless 是 C:\useless 别名 <br/>
useless=C:\useless<br/>

chrome_cache=V:\chrome_cache<br/>

;{useless}/I 是junction 的target 文件夹，最终的文件夹路径为 C:\useless\I ,
;注意两种路径分隔符 / \ 都可以使用或混合使用 <br/>
;{chrome_cache}/A 是junction 的 source 文件夹，最终还原成的文件夹路径为 V:\chrome_cache\A<br/>
;下面一段配置的意思是：<br/>
;这三个文件夹 {chrome_cache}/A,{chrome_cache}/B,{chrome_cache}/C 都 <br/>
;junction 到 {useless}/I 文件下。 

;另外{chrome_cache}/A 等左边的 <br/>
;续号01,02,03没有太多意义是用来保证 ini 文件键、值配置项完整性<br/>
;因为ini配置文件要求： <br/>
;键、值不能缺少或为空 ；这里只要保证每一个节下的键不重复即可。 <br/>
[{useless}/I] <br/>
01={chrome_cache}/A<br/> 
02={chrome_cache}/B <br/>
03={chrome_cache}/C<br/>

;配置项可以用多个，如下 <br/>
[{useless}/J] <br/>
01={chrome_cache}/K<br/> 
02={chrome_cache}/L <br/>
03={chrome_cache}/M <br/>
04={chrome_cache}/N<br/>