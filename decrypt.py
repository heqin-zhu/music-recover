#coding : utf-8
import os
import sys
import glob
import requests
import mutagen

from mutagen.id3 import ID3, APIC, TIT2, TPE1, TRCK, TALB, USLT, error
# ID3 info:
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

hasModu = False
try:
    from mutagen.easyid3 import EasyID3
    from mutagen.mp3 import MP3
    hasModu = True
except:
    pass

def safeprint(s):
    '''deal with invalid encoded filename'''
    try:
        print(s)
    except:
        print(repr(s)[1:-1])

class netease_music:
    def __init__(self, path=''):
        '''path is the direcoty that contains Music files(cached)'''
        if path == '':
            path = input('input the path of cached netease_music')
        self.path = path
        safeprint('[+] Current Path: ' + path)
        safeprint('[+] Output Path: ' + MSCDIR)
        os.chdir(path)
        self.files = glob.glob('*.uc') + glob.glob('*.uc!')
        self.id_mp = {}
        for i in self.files:
            self.id_mp[self.getId(i)] = i
        if not os.path.exists(MSCDIR):
            os.mkdir(MSCDIR)
        # import re
        # self.nameXpath ='//div[@class="tit"]/em[@class="f-ff2"]/text()'
        # self.lrcSentencePt=re.compile(r'\[\d+:\d+\.\d+\](.*?)\\n')         # wrong  (r'\[\d+,\d+\](\(\d+,\d+\)(\w))+\n')

    def getId(self, name):
        return name[:name.find('-')]

    def getInfoFromWeb(self, musicId):
        dic = {}
        url = 'http://music.163.com/api/song/detail/?ids=[' + musicId + ']'
        res = requests.get(url, headers = headers).json()
        info = res['songs'][0]
        dic['artist'] = [info['artists'][0]['name']]
        dic['title'] = [info['name']]
        dic['cover'] = [info['album']['picUrl']]
        dic['album'] = [info['album']['name']]
        return dic

    def getInfoFromFile(self, path):
        if not os.path.exists(path):
            safeprint('Can not find file ' + path)
            return {}
        elif hasModu:
            return dict(MP3(path, ID3=EasyID3))
        else:
            print('[Error] You can use pip3 to install mutagen or connet to the Internet')
            raise Exception('Failed to get info of ' + path)

    def getPath(self, dic, musicId):
        title = dic['title'][0]
        artist = dic['artist'][0]
        if artist in title:
            title = title.replace(artist, '').strip()
        name = artist + ' - ' + title
        for i in '>?*/\:"|<':
            name = name.replace(i,'-') # form valid file name
        self.id_mp[musicId] = name
        #print('''{{title: "{title}",artist: "{artist}",mp3: "http://ounix1xcw.bkt.clouddn.com/{name}.mp3",cover: "{cover}",}},'''\
               #.format(title = title,name = name,artist=artist,cover=dic['cover'][0]))
        return os.path.join(MSCDIR, name + '.mp3')
    
    def decrypt(self, cachePath):
        musicId = self.getId(cachePath)
        idpath = os.path.join(MSCDIR, musicId + '.mp3')
        try:  # from web
            info = self.getInfoFromWeb(musicId)
            path = self.getPath(info, musicId)
            if not os.path.exists(path):
                with open(path,'wb') as f:
                    f.write(bytes(self._decrypt(cachePath)))
        except Exception as e:  # from file
            print(e)
            if not os.path.exists(idpath):
                with open(idpath,'wb') as f:
                    f.write(bytes(self._decrypt(cachePath)))
            info = self.getInfoFromFile(idpath)
            path = self.getPath(info, musicId)
            if os.path.exists(path):
                os.remove(idpath)
            else:
                os.rename(idpath, path)
        return info, path

    def _decrypt(self,cachePath):
        with open(cachePath, 'rb') as f:
            btay = bytearray(f.read())
        for i, j in enumerate(btay):
            btay[i] = j ^ 0xa3
        return btay

    def getLyric(self, musicId):
        name = self.id_mp[musicId]
        url = 'http://music.163.com/api/song/lyric?id='+ musicId +'&lv=1&kv=1&tv=-1'
        try:
            lrc = requests.get(url).json()['lrc']['lyric']
            if lrc=='':
                raise Exception('')

            return lrc
            # write lrc file
            # LRCDIR = os.path.join(MSCDIR, 'lyric')
            # if not os.path.exists(LRCDIR):
            #     os.mkdir(LRCDIR)
            # file = os.path.join(LRCDIR, name + '.lrc')
            # if not os.path.exists(file):
            #     with open(file, 'w', encoding='utf8') as f:
            #         f.write(str(lrc))
        except Exception as e:
            safeprint('{} Failed to get lyric of music. Line {}: {}'.format(name, format(sys.exc_info()[-1].tb_lineno), e))

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
            tags.add(TPE1(encoding=3, lang='', desc='', text=info['artist'][0]))

        for key,values in tags.items():
            print('\t', key, ': ', values, sep='')

        tags.add(USLT(encoding=3, lang='eng', desc='aaa', text=lrc))
        tags.save()

    def getMusic(self):
        for ct, cachePath in enumerate(self.files):
            info, path = self.decrypt(cachePath)
            musicId = self.getId(cachePath)
            print('[{}]'.format(ct+1).ljust(5)+self.id_mp[musicId])
            self.setID3(self.getLyric(musicId), info, path)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1].strip()
    if len(sys.argv) > 2:
        MSCDIR = sys.argv[2]
    handler = netease_music(path)
    handler.getMusic()
