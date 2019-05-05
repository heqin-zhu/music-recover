<div align="center">
    <h1>netease-music-cracker</h1>
    <br>
    <img src="images/logo.png">
</div>

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
![warning](images/warning.png)

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
![](images/flow-chart.png)

(我没有在 linux 上用过 网易云音乐, 所以我现在不知道路径, 需要使用者自己找, 欢迎知道的同学告诉我)

我上传了示例文件在 `music`中, 
可以运行
`python3 decrypt.py music` 尝试

## 展示
![](images/display.gif)

结果在文件夹`网易云音乐缓存:smiley: 
## 贡献
Pull request

[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/0)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/0)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/1)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/1)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/2)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/2)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/3)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/3)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/4)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/4)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/5)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/5)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/6)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/6)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/7)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/7)

