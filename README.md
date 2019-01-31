# netease-music-cracker
[![Stars](https://img.shields.io/github/stars/mbinary/netease-music-cracker.svg?label=Stars&style=social)](https://github.com/mbinary/netease-music-cracker/stargazers)
[![Forks](https://img.shields.io/github/forks/mbinary/netease-music-cracker.svg?label=Fork&style=social)](https://github.com/mbinary/netease-music-cracker/network/members)
[![repo-size](https://img.shields.io/github/repo-size/mbinary/netease-music-cracker.svg)]()
[![License](https://img.shields.io/badge/LICENSE-MIT-blue.svg)](LICENSE)
[![Language](https://img.shields.io/badge/language-python3.6-orange.svg)]()
[![Build](https://travis-ci.org/mbinary/netease-music-cracker.svg?branch=master)]()
[![Coverage](https://codecov.io/gh/mbinary/netease-music-cracker/branch/master/graph/badge.svg)]()
<!--  [![License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)  copy LICENCE -->
<!-- 控制图片: <img width="60" height="75" align="right" src="haha"> -->
# 前言
![warning](src/warning.png)

网易云音乐的缓存文件经过处理,也就是异或加密了的,要获得MP3文件,需要解密. 这个仅用于学习. 请大家**尊重版权**.其实大多数歌曲都是可以下载的

## 介绍
从网易云音乐缓存文件得到 mp3 格式. 
利用缓存文件,解密得到MP3文件, 并通过其metadata,命名文件,顺便从api或者网页抓取歌词,详细介绍可以看[这里](https://mbinary.coding.me/decrypt-netease-music.html) 

## 依赖
* python3
* python 模块
  - requests
  - mutagen (optional)
运行 如下命令安装
```shell
$ sudo apt-get install python3
$ pip install -r requirements.txt
```

## 使用
### 先找到缓存文件路径
mac pro or windows 使用者 可以跳过此步骤(因为我知道路径  (●ˇ∀ˇ●))


- linux
- 手机:  将`/netease/cloudmusic/Cache/Music1`文件夹复制到电脑上, 记为
- 以及运行过程中出现'Path not found', 'No cache file'的使用者

找到后缀为 .uc!, .uc的文件夹即可.  (我没有在 linux 上用过 网易云音乐, 所以我现在不知道路径, 需要使用者自己找, 欢迎知道的同学告诉我)

然后修改 config.py 文件中 `SRCDIR` 那一行(最后一行).
例如 你找到路径为`/music/cache`,  则修改为 `SRCDIR = '/music/cache'` (行首不要有多余的空白)

### 运行
- 命令行
```shell
$ python3 decrypt.py
```
- python 程序 直接运行


我在 这个 repo 里面上传了几个缓存文件,可以作为测试,在 [Music1](Music1) 中

## 展示
![](src/display.gif)

## 结果
在当前目录(运行此脚本的目录)中得到`cached_网易云音乐`:smiley: 

* 输出
 ![](src/result.jpg)

* 歌词
 ![](src/lyric.jpg)

* MP3
 ![](src/music.jpg)
