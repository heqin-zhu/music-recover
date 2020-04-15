<div align="center">
    <h1>netease-music-cracker</h1>
    <br>
    <img src="images/logo.png">
</div>

[![Stars](https://img.shields.io/github/stars/mbinary/netease-music-cracker.svg?label=Stars&style=social)](https://github.com/mbinary/netease-music-cracker/stargazers)
[![Forks](https://img.shields.io/github/forks/mbinary/netease-music-cracker.svg?label=Fork&style=social)](https://github.com/mbinary/netease-music-cracker/network/members)
[![License](https://img.shields.io/badge/LICENSE-MIT-blue.svg)](LICENSE)
[![Contributors](https://img.shields.io/github/contributors/mbinary/netease-music-cracker.svg)](https://github.com/mbinary/netease-music-cracker/graphs/contributors)
[![Language](https://img.shields.io/badge/language-python3.5-orange.svg)](.)
[![Build](https://travis-ci.org/mbinary/netease-music-cracker.svg?branch=master)](https://travis-ci.org/mbinary/netease-music-cracker?branch=master)
[![Coverage](https://codecov.io/gh/mbinary/netease-music-cracker/branch/master/graph/badge.svg)](https://codecov.io/github/mbinary/netease-music-cracker?branch=master)
[![codebeat badge](https://codebeat.co/badges/875e7de3-895b-479e-9384-c5db71930c15)](https://codebeat.co/projects/github-com-mbinary-netease-music-cracker-master)
<!--  [![License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)  copy LICENCE -->
<!-- 控制图片: <img width="60" height="75" align="right" src="haha"> -->
# 声明
![warning](images/warning.png)

代码仅供技术交流，参考学习，请尊重版权,勿用于商业及非法用途，如产生法律纠纷与本人无关

## 介绍
从缓存文件得到 mp3 文件。这是[详细介绍](https://mbinary.xyz/decrypt-netease-music.html) 

## 依赖
* python3.5+
* python 模块
  - requests
  - mutagen

运行 如下命令安装
```shell
$ pip3 install -r requirements.txt
```

## 使用
![](images/flow-chart.png)

- 如果要获得电脑上的缓存文件，那么可以不传入参数直接运行这个脚本`python3 decrypt.py`
- 如果是手机上的（`一般是netease/cloudmusic[lite]/Cache/Music1`, 将其拷贝到电脑上），**或者上面情况出现没有找到文件夹，没有文件等错误**，那么需要指定缓存文件的位置作为参数运行(可以将缓存文件夹拷贝到当前目录重命名music, 然后运行`python3 decrypt.py music`)。
- 已上传示例文件，可运行`python3 decrypt.py music` 进行尝试
- 结果保存在当前目录下的`mp3`中:smiley: 

## 贡献
[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/0)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/0)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/1)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/1)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/2)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/2)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/3)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/3)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/4)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/4)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/5)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/5)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/6)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/6)[![](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/images/7)](https://sourcerer.io/fame/mbinary/mbinary/netease-music-cracker/links/7)
