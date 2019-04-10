# coding : utf-8
from __future__ import print_function
import os
import sys
import getpass
import requests

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, USLT  # error
# ID3 info:

# two args: id  type
# type=song, lyric, comments, detail, artist, album, search
# eg  API = 'https://api.imjad.cn/cloudmusic/?type=song&id=1234132'    download music
# APIC: picture
# TIT2: title
# TPE1: artist
# TRCK: track number
# TALB: album
# USLT: lyric

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MSCDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '网易云音乐缓存')
headers = {'User-agent': 'Mozilla/5.0'}
'''
1def safeprint(s):
    #deal with invalid encoded filename
    try:
        print(s)
    except:
        print(repr(s)[1:-1])
'''


class netease_music:
    def __init__(self, path=''):
        '''path is the direcoty that contains Music files(cached)'''
        while not os.path.exists(path):
            path = input('Input the correct directory of cached netease_music')
        if len(os.listdir(path)) == 0:
            raise Exception('No cache file found, change a directory')
        self.path = path
        print('[+] Saved in: ' + MSCDIR)
        self.files = [
            i for i in os.listdir(path)
            if i.endswith('.uc') or i.endswith('.uc!')
        ]
        self.id_name = {self.getId(i): i for i in self.files}
        self.name_id = {j: i for i, j in self.id_name.items()}
        if not os.path.exists(MSCDIR):
            os.mkdir(MSCDIR)
        # self.nameXpath ='//div[@class="tit"]/em[@class="f-ff2"]/text()'
        # self.lrcSentencePt=re.compile(r'\[\d+:\d+\.\d+\](.*?)\\n')         # wrong  (r'\[\d+,\d+\](\(\d+,\d+\)(\w))+\n')

    def getId(self, name):
        return name[:name.find('-')]

    def getInfoFromWeb(self, musicId):
        dic = {}
        url = 'http://music.163.com/api/song/detail/?ids=[' + musicId + ']'
        res = requests.get(url, headers=headers).json()
        info = res['songs'][0]
        dic['artist'] = [info['artists'][0]['name']]
        dic['title'] = [info['name']]
        dic['cover'] = [info['album']['picUrl']]
        dic['album'] = [info['album']['name']]
        return dic

    def getName(self, dic, musicId):
        '''get the name of music from info dict'''
        title = dic['title'][0]
        artist = dic['artist'][0]
        if artist in title:
            title = title.replace(artist, '').strip()
        name = artist + ' - ' + title
        for i in '>?*/\\:"|<':
            name = name.replace(i, '-')  # form valid file name
        self.id_name[musicId] = name
        #print('''{{title: "{title}",artist: "{artist}",mp3: "http://ounix1xcw.bkt.clouddn.com/{name}.mp3",cover: "{cover}",}},'''\
        #.format(title = title,name = name,artist=artist,cover=dic['cover'][0]))
        return os.path.join(MSCDIR, name + '.mp3')

    def decrypt(self, name):
        cachePath = os.path.join(self.path, name)
        musicId = self.name_id[name]
        idpath = os.path.join(MSCDIR, musicId + '.mp3')
        if not os.path.exists(idpath):
            with open(idpath, 'wb') as f:
                f.write(bytes(self._decrypt(cachePath)))
        try:  # from web
            info = self.getInfoFromWeb(musicId)
        except Exception as e:  # from file
            #print(e, ' at line {}'.format(sys.exc_info()[-1].tb_lineno))
            info = dict(MP3(path, ID3=EasyID3))

        path = self.getName(info, musicId)
        if os.path.exists(path):
            os.remove(idpath)
        else:
            os.rename(idpath, path)
        return info, path

    def _decrypt(self, cachePath):
        with open(cachePath, 'rb') as f:
            btay = bytearray(f.read())
        for i, j in enumerate(btay):
            btay[i] = j ^ 0xa3
        return btay

    def getLyric(self, musicId):
        url = 'http://music.163.com/api/song/lyric?id=' + musicId + '&lv=1&kv=1&tv=-1'
        try:
            return requests.get(url).json()['lrc']['lyric']
        except:
            return ''

    def setID3(self, lrc, info, path):
        tags = ID3(path)
        # remove old unsychronized lyrics
        if len(tags.getall("USLT")) != 0:
            tags.delall("USLT")

        dic = {'title': TIT2, 'artist': TPE1, 'album': TALB}

        for k, T in dic.items():
            if k in info:
                tags.add(T(encoding=3, lang='', desc='', text=info[k][0]))
        if ('cover' in info):
            tags.add(
                APIC(
                    encoding=3,
                    mime='image/png',
                    type=3,
                    desc='cover',
                    data=requests.get(info['cover'][0],
                                      stream=True).raw.read()))

        for key in dic:
            li = tags[dic[key].__name__].text
            print('\t{}: {}'.format(key.ljust(6), ', '.join(li) ))

        tags.add(USLT(encoding=3, text=lrc))
        tags.save()

    def getMusic(self):
        for ct, name in enumerate(self.files):
            info, path = self.decrypt(name)
            musicId = self.name_id[name]
            print('[{}]'.format(ct + 1).ljust(5) + self.id_name[musicId])
            self.setID3(self.getLyric(musicId), info, path)


if __name__ == '__main__':
    platform = os.sys.platform.lower()
    user = getpass.getuser()
    path = ''
    if len(sys.argv) > 1:
        path = sys.argv[1].strip()
    elif platform.startswith('win'):
        path = 'C:/Users/{user}/AppData/Local/Netease/CloudMusic/Cache/Cache'.format(
            user=user)
    #elif platform.startswith('linux'):
    else:  # macpro
        path = '/Users/macbookpro({})/Library/Containers/com.netease.163music/Data/Caches/online_play_cache'.format(
            user=user)
    handler = netease_music(os.path.abspath(path))
    handler.getMusic()
