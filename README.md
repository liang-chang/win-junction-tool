# win-junction-tool

batch create ntfs junction

功能：批量创建 junction 的工具

一些软件比如 QQ , 开发用的IDE会大量的往硬盘写些文件，而这些文件通常是无用的日志文件类，大量的io还会拖慢系统。 一个比较好的解决方法是，创建 ramdisk 并把这些文件夹定向到ramdisk 上，利用 ramdisk 的高速及重启还原的特性，使这些无用的文件对系统的影响降到最小，同时也避免过多写入垃圾文件，减小清理。 那个文件夹重定向的功能就是 windows ntfs junction ，类似linux 上的软链接。

系统：windows xp/vista/7 (win 8/10 没有试验) 需要的环境：python 3

Q&A 1.为什么要用 python3 做为运行环境？ 因为之前我在学python3，为了熟悉python3，所以我选用了python3作为运行环境。

配置文件 config.ini 介绍：

[config] ; 原始文件夹是否重命名备份，重命令名的规则添加 _link_bak 后缀 renameOriginFolder = true

; 是否清空原始文件夹 clearOriginFolder = false

;当目录文件夹无效时是否跳过，当target文件夹无效时，false 会终止运行；否则跳过 skipInvalidTarget = false

;当源文件夹不存在，且父文件夹不存在时是否还要创建；false 不创建；true 会继续创建 createSourceParent=false

;pathAlias 是给一些反复使用的文件夹起别名，内置了两个别名， UserHome 和 Temp ，分别指向用户目录和系统临时文件夹; ;下面要引用该文件时，只需要把名称用大括号包起来，比如引用 Temp 该这样使用： {Temp} [pathAlias] ;build in path variable ; UserHome ; Temp

;useless 是 C:\useless 别名 useless=C:\useless

chrome_cache=V:\chrome_cache

;{useless}/I 是junction 的target 文件夹，最终的文件夹路径为 C:\useless\I , 两种分隔符 / \ 都可以 ;{chrome_cache}/A 是junction 的 source 文件夹，最终的文件夹路径为 V:\chrome_cache\A , 两种分隔符 /\ 都可以 ;以下该配置项表示该配置下所有的文件夹包括 {chrome_cache}/A,{chrome_cache}/B,{chrome_cache}/C 都 ;junction 到 {useless}/I 文件下。 {chrome_cache}/A,{chrome_cache}/B,{chrome_cache}/C 左边的 ;续号01,02,03没有太多意义是用来保证 ini 文件键、值配置项完整，因为ini配置文件要求： ;键、值不能缺少或为空 ；这里只要保证每一个节下的键不重复即可。 [{useless}/I] 01={chrome_cache}/A 02={chrome_cache}/B 03={chrome_cache}/C

;配置项可以用多个，如下 [{useless}/J] 01={chrome_cache}/K 02={chrome_cache}/L 03={chrome_cache}/M 04={chrome_cache}/N
