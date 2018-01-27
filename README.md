![warning](http://ounix1xcw.bkt.clouddn.com/warning.png)
（学习使用异或加密 :see_no_evil:

下面是使用说明书

# 用途
用于获取网易云音乐缓存文件的歌曲
在手机上的缓存文件在 `netease/cloudmusic/Cache/`里的`Music1`里， 歌词在`Lyric`里，（电脑上的路径可以在设置里找到）


# 运行条件
* python3
* python 模块安装
  - mutagen
  - lxml
  - requests
  - json
  
 可以pip install 安装，常见问题可以自行搜索解决
 
 # 缓存文件
 找到缓存文件的路径， 形如`...../netease/cloudmusic/Cache/Music1`，如果想单独复制过来，请复制 `Music1`和`Lyric`文件夹在同一目录下，再得到路径,
 
 # 运行
 ## 在命令行模式下
 python3 netease-music.py  *path*
 
 如果不在 netease-music.py所在目录下，可以切换到，或者用它的绝对路径，
 path是上一步得到的路径
 
 ## 代码中
 可以打开代码文件然后修改path，然后运行即可
 
 # 结果
 你就可以到Music1所在目录下的`cached_网易云音乐`看到lyric, music了 :smiley: 
