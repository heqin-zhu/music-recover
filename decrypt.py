# coding : utf-8
import urllib3
import os
import sys
import getpass
import requests

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, USLT

# ID3 info:
keyMap = {'APIC': 'cover',
          'TIT2': 'title',
          'TPE1': 'artist',
          'TRCK': 'track',
          'TALB': 'album',
          'USLT': 'lyric'
          }
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {'User-agent': 'Mozilla/5.0'}
VERBOSE = False
MSCDIR = os.path.abspath('./网易云音乐缓存')
# '''deal with invalid encoded filename'''
# print(repr(s)[1:-1])


class netease_music:
    def __init__(self, path=''):
        '''path: direcoty that contains cache files'''
        self.path = path
        self.files = [i for i in os.listdir(
            path) if i.endswith('.uc') or i.endswith('.uc!')]
        if self.files == []:
            print('No cache file found in "{}"'.format(path))
        else:
            if not os.path.exists(MSCDIR):
                os.mkdir(MSCDIR)
            print('[ ]   Output Path: ' + MSCDIR)
        self.id_name = {self.getId(i): i for i in self.files}
        self.name_id = {j: i for i, j in self.id_name.items()}

    def getId(self, name):
        return name[:name.find('-')]

    def getInfoFromFile(self, path):
        return dict(MP3(path, ID3=EasyID3))

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
        if artist in title:
            title = title.replace(artist, '').strip()
        name = artist + ' - ' + title
        for i in '>?*/\:"|<':
            name = name.replace(i, '-')  # convert to valid chars for file name
        self.id_name[musicId] = name
        return os.path.join(MSCDIR, name + '.mp3')

    def decrypt(self, name):
        cachePath = os.path.join(self.path, name)
        musicId = self.name_id[name]
        idpath = os.path.join(MSCDIR, musicId + '.mp3')
        try:  # from web
            info = self.getInfoFromWeb(musicId)
            path = self.getPath(info, musicId)
            if not os.path.exists(path):
                with open(path, 'wb') as f:
                    f.write(bytes(self._decrypt(cachePath)))
        except Exception as e:  # from file
            print(e)
            if not os.path.exists(idpath):
                with open(idpath, 'wb') as f:
                    f.write(bytes(self._decrypt(cachePath)))
            try:
                info = self.getInfoFromFile(idpath)
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
                path = ''
        return info, path

    def _decrypt(self, cachePath):
        with open(cachePath, 'rb') as f:
            btay = bytearray(f.read())
        for i, j in enumerate(btay):
            btay[i] = j ^ 0xa3
        return btay

    def getLyric(self, musicId):
        url = 'http://music.163.com/api/song/lyric?id=' + musicId + '&lv=1&tv=-1'
        try:
            lyric = requests.get(url).json()
            lrc = lyric['lrc']['lyric']
            if lrc == '':
                raise Exception('')

            tlrc = lyric['tlyric']['lyric']
            if tlrc:
                # 多种语言歌词合并
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
                s = []
                for k, v in sorted(dicCopy.items(), key=lambda item: item[0]):
                    s.append("[%s]%s" % (k.strip(), v))
                lrc = "\n".join(s)
            return lrc
        except Exception as e:
            if VERBOSE:
                print('No lyric found')
            return ''

    def setID3(self, lrc, info, path):
        tags = ID3(path)
        # remove old unsychronized lyrics
        if len(tags.getall("USLT")) != 0:
            tags.delall("USLT")

        if ('album' in info):
            tags.add(TALB(encoding=3, lang='', desc='', text=info['album'][0]))
        if ('title' in info):
            tags.add(TIT2(encoding=3, lang='', desc='', text=info['title'][0]))
        if ('artist' in info):
            tags.add(TPE1(encoding=3, lang='',
                          desc='', text=info['artist'][0]))
        if ('cover' in info):
            tags.add(APIC(
                encoding=3,
                mime='image/png',
                type=3,
                desc='cover',
                data=requests.get(info['cover'][0], stream=True).raw.read()
            ))
        tags.add(USLT(encoding=3, lang='eng', desc='aaa', text=lrc))
        tags.save()

    def getMusic(self):
        for ct, name in enumerate(self.files):
            musicId = self.name_id[name]
            info, path = self.decrypt(name)
            if os.path.exists(path):
                print('[{}]'.format(ct+1).ljust(6) + self.id_name[musicId])
                try:
                    self.setID3(self.getLyric(musicId), info, path)
                except Exception as e:
                    if VERBOSE:
                        print('Set metadata Failed: ', e)


if __name__ == '__main__':
    platform = os.sys.platform.lower()
    user = getpass.getuser()
    path = ''
    if len(sys.argv) > 1:
        path = os.path.abspath(sys.argv[1].strip())
    elif platform.startswith('win'):
        path = 'C:/Users/{user}/AppData/Local/Netease/CloudMusic/Cache/Cache'.format(
            user=user)
    else:  # mac or linux
        pre = ''
        segs = os.getcwd().split(os.sep)
        if len(segs) >= 3:
            pre = os.sep.join(segs[:3])
        if not os.path.exists(pre):
            pre = '/Users/' + user
        path = os.path.join(
            pre, 'Library/Containers/com.netease.163music/Data/Caches/online_play_cache')
    if not os.path.exists(path):
        raise Exception('[Error] Directory "{}" does not exist'.format(path))
    else:
        netease_music(path).getMusic()
