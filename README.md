
# forked from mbinary/netease-cached-music
[+] MP3 嵌入歌词

# 网易云音乐缓存文件 --> MP3
>网易云音乐的缓存文件经过处理,也就是异或加密了的,要获得MP3文件,需要解密. 这个仅用于学习. 请大家尊重音乐的版权.其实大多数歌曲都是可以下载的

## 需求
* python3
* python 模块
  - requests
  - mutagen

可以pip3 install 安装

## 使用
将缓存目录拖动到 decrypt.bat 即可, 例 `D:\CloudMusic\Cache`

### 获得缓存文件
下面两种方法都行
* 手机上的在 `netease/cloudmusic/Cache/Music1`里,将其复制到电脑上
* 或者在电脑上 `**/cloudmusicdata/Cache`.

最终得到的路径为当前目录下 `网易云音乐缓存`

### 运行
下面两种方法都行
* 在命令行模式下
`python3 decrypt.py {MUSIC}`

这里的 `MUSIC`  就是缓存目录（包含`.uc` 或 `.uc!` 文件）的地址, 例 `D:\CloudMusic\Cache`

## Licence
[MIT](LICENCE)
