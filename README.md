# netease-music-cracker
[![Stars](https://img.shields.io/github/stars/mbinary/netease-music-cracker.svg?label=Stars&style=social)](https://github.com/mbinary/netease-music-cracker/stargazers)
[![Forks](https://img.shields.io/github/forks/mbinary/netease-music-cracker.svg?label=Fork&style=social)](https://github.com/mbinary/netease-music-cracker/network/members)
[![License](https://img.shields.io/badge/LICENSE-MIT-blue.svg)](LICENSE)
[![Contributors](https://img.shields.io/github/contributors/mbinary/netease-music-cracker.svg)](https://github.com/mbinary/netease-music-cracker/graphs/contributors)
[![Language](https://img.shields.io/badge/language-python3.6-orange.svg)](.)
[![Build](https://travis-ci.org/mbinary/netease-music-cracker.svg?branch=master)](https://travis-ci.org/mbinary/netease-music-cracker?branch=master)
[![Coverage](https://codecov.io/gh/mbinary/netease-music-cracker/branch/master/graph/badge.svg)](https://codecov.io/github/mbinary/netease-music-cracker?branch=master)
[![codebeat badge](https://codebeat.co/badges/952ebbfc-770d-4b12-bfdf-b03ef76c5912)](https://codebeat.co/projects/github-com-mbinary-netease-music-cracker-master)
<!--  [![License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)  copy LICENCE -->
<!-- 控制图片: <img width="60" height="75" align="right" src="haha"> -->
# 前言
![warning](src/warning.png)

网易云音乐的缓存文件经过处理,也就是异或加密了的,要获得MP3文件,需要解密. 这个仅用于学习. 请大家**尊重版权**.其实大多数歌曲都是可以下载的

## 介绍
从网易云音乐缓存文件得到 mp3 格式. 
利用缓存文件,解密得到MP3文件, 并通过其metadata,命名文件,顺便从api或者网页抓取歌词,详细介绍可以看[这里](https://mbinary.coding.me/decrypt-netease-music.html) 

## 依赖
* python 模块
  - requests
  - mutagen

运行 如下命令安装
```shell
$ pip install -r requirements.txt
```

## 使用
![](src/flow-chart.png)

(我没有在 linux 上用过 网易云音乐, 所以我现在不知道路径, 需要使用者自己找, 欢迎知道的同学告诉我)

我上传了两个示例文件在 `src/music`中, 
可以运行
`python3 decrypt.py src/music` 尝试

## 展示
![](src/display.gif)

## 结果
在当前目录(运行此脚本的目录)中, 生成文件夹`网易云音乐缓存`, 结果就在其中:smiley: 

