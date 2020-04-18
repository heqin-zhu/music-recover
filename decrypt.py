# coding : utf-8
import re
import os
import sys
import getpass
import urllib3
import requests

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, USLT

# ID3 info:
tagMap = {'cover': APIC, 'title': TIT2,
          'artist': TPE1, 'album': TALB, 'lyric': USLT}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {'User-agent': 'Mozilla/5.0'}
MSCDIR = './mp3'
# print(repr(s)[1:-1])  # deal with invalid encoded filename


class netease_music:
    def __init__(self, path=''):
        '''path: direcoty that contains cache files'''
        self.path = path
        self.id_name = {i[:i.find('-')]: i for i in os.listdir(path)
                        if i.endswith('.uc') or i.endswith('.uc!')}
        if self.id_name:
            if not os.path.exists(MSCDIR):
                os.mkdir(MSCDIR)
            print('Input :', path)
            print('Output:', MSCDIR)
        else:
            print('No cache file found in "{}"'.format(path))

    def getInfoFromWeb(self, musicId):
        # xpath for name and lrc:
        # self.nameXpath ='//div[@class="tit"]/em[@class="f-ff2"]/text()'
        # self.lrcSentencePt=re.compile(r'\[\d+:\d+\.\d+\](.*?)\\n')         # wrong  (r'\[\d+,\d+\](\(\d+,\d+\)(\w))+\n')

        # api :
        # type=song, lyric, comments, detail, artist, album, search
        # eg  API = 'https://api.imjad.cn/cloudmusic/?type=song&id=1234132'    download music

        dic = {}
        url = 'http://music.163.com/api/song/detail/?ids=[' + musicId + ']'
        res = requests.get(url, headers=headers).json()
        info = res['songs'][0]
        dic['artist'] = [info['artists'][0]['name']]
        dic['title'] = [info['name']]
        dic['cover'] = [info['album']['picUrl']]
        dic['album'] = [info['album']['name']]
        return dic

    def getPath(self, dic, musicId):
        '''get the name of music from info dict'''
        title = dic['title'][0]
        artist = dic['artist'][0]
        name = title + '(' + artist+')'
        for i in '>?*/\:"|<':
            name = name.replace(i, '-')  # convert to valid chars for file name
        name = re.sub('\s', '_',name)
        self.id_name[musicId] = name
        return os.path.join(MSCDIR, name + '.mp3')

    def decrypt(self, musicId, name):
        def _decrypt(cachePath):
            with open(cachePath, 'rb') as f:
                btay = bytearray(f.read())
            for i, j in enumerate(btay):
                btay[i] = j ^ 0xa3
            return btay
        cachePath = os.path.join(self.path, name)
        idpath = os.path.join(MSCDIR, musicId + '.mp3')
        info = self.getInfoFromWeb(musicId)
        path = self.getPath(info, musicId)
        if not os.path.exists(path):
            with open(path, 'wb') as f:
                f.write(bytes(_decrypt(cachePath)))

        '''  get info from index file
        if not os.path.exists(idpath):
            with open(idpath, 'wb') as f:
                f.write(bytes(_decrypt(cachePath)))
        try:
            info = dict(MP3(idpath, ID3=EasyID3))
        except:
            info = {}
        if info != {}:
            path = self.getPath(info, musicId)
            if os.path.exists(path):
                os.remove(idpath)
            else:
                os.rename(idpath, path)
        else:
            os.remove(idpath)
        '''
        return info, path

    def getLyric(self, musicId):
        url = 'http://music.163.com/api/song/lyric?id=' + musicId + '&lv=1&tv=-1'
        lrc = ''
        try:
            lyric = requests.get(url, headers=headers).json()
            lrc = lyric['lrc']['lyric']
            tlrc = lyric['tlyric']['lyric']
            # merge multi-lang lyrics
            dic = {}
            for i in lrc.splitlines():
                a = i.replace('[', ']').strip().split("]")
                dic[a[1].strip()+' '] = a[-1].strip()
            tdic = {}
            for m in tlrc.splitlines():
                n = m.replace('[', ']').strip().split(']')
                tdic[n[1].strip()] = n[-1].strip()
            dicCopy = dic.copy()
            dicCopy.update(tdic)
            lines = []
            for k, v in sorted(dicCopy.items(), key=lambda item: item[0]):
                lines.append("[%s]%s" % (k.strip(), v))
            lrc = "\n".join(lines)
        except Exception as e:
            pass
        return lrc

    def setID3(self, lrc, info, path):
        tags = ID3(path)
        # remove old unsychronized lyrics
        len(tags.getall("USLT")) != 0 and tags.delall("USLT")
        for t in ['album', 'title', 'artist']:
            t in info and tags.add(
                tagMap[t](encoding=3, lang='', desc='', text=info[t][0]))
        'cover' in info and tags.add(APIC(
            encoding=3,
            mime='image/png',
            type=3,
            desc='cover',
            data=requests.get(info['cover'][0], stream=True,
                              headers=headers).raw.read()
        ))
        tags.add(USLT(encoding=3, lang='eng', desc='aaa', text=lrc))
        tags.save()

    def getMusic(self):
        ct = 0  # count successed files
        for musicId, name in self.id_name.items():
            try:
                info, path = self.decrypt(musicId, name)
                ct += 1
                print('[{}]'.format(ct).ljust(6) + self.id_name[musicId])
                self.setID3(self.getLyric(musicId), info, path)
            except Exception as e:
                pass


if __name__ == '__main__':
    platform = os.sys.platform.lower()
    user = getpass.getuser()
    pre = '/'.join(os.getcwd().split(os.sep)[:3])
    if len(sys.argv) > 1:
        path = os.path.abspath(sys.argv[1].strip())
    elif platform.startswith('win'):  # windows
        path = pre + '/AppData/Local/Netease/CloudMusic/Cache/Cache'

    else:  # mac or linux
        path = pre + '/Library/Containers/com.netease.163music/Data/Caches/online_play_cache'
    if os.path.exists(path):
        netease_music(path).getMusic()
    else:
        print('Directory "{}" does not exist, specify cache files directory instead'.format(path))
