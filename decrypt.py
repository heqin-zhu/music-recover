#coding : utf-8
import os
import sys
import getpass
import requests

from config import *

# two args: id  type
# type=song, lyric, comments, detail, artist, album, search
# eg  API = 'https://api.imjad.cn/cloudmusic/?type=song&id=1234132'    download music

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
        self.files =[i for i in os.listdir(path) if i.endswith('.uc') or i.endswith('.uc!')]
        self.id_name = {self.getId(i):i for i in self.files}
        self.name_id = {j:i for i,j in self.id_name.items()}
        for dr in [DESDIR,LRCDIR,MSCDIR]:
            if not os.path.exists(dr):
                os.mkdir(dr)
        # import re
        # self.nameXpath ='//div[@class="tit"]/em[@class="f-ff2"]/text()'
        # self.lrcSentencePt=re.compile(r'\[\d+:\d+\.\d+\](.*?)\\n')         # wrong  (r'\[\d+,\d+\](\(\d+,\d+\)(\w))+\n')

    def getId(self, name):
        return name[:name.find('-')]

    def getInfoFromWeb(self, musicId):
        dic = {}
        url = API+'type=detail&id=' + musicId
        info = requests.get(url).json()['songs'][0]
        dic['artist'] = [info['ar'][0]['name']]
        dic['title'] = [info['name']]
        dic['cover'] = [info['al']['picUrl']]
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

    def getPath(self, dic,musicId):
        '''get the name of music from info dict'''
        title = dic['title'][0]
        artist = dic['artist'][0]
        if artist in title:
            title = title.replace(artist, '').strip()
        name = (title + '--' + artist)
        for i in '>?*/\:"|<':
            name = name.replace(i,'-') # form valid file name
        self.id_name[musicId] = name
        #print('''{{title: "{title}",artist: "{artist}",mp3: "http://ounix1xcw.bkt.clouddn.com/{name}.mp3",cover: "{cover}",}},'''\
               #.format(title = title,name = name,artist=artist,cover=dic['cover'][0]))
        return os.path.join(MSCDIR, name + '.mp3')
    
    def decrypt(self, name):
        cachePath = os.path.join(self.path,name)
        musicId = self.name_id[name]
        idpath = os.path.join(MSCDIR, musicId + '.mp3')
        try:  # from web
            dic = self.getInfoFromWeb(musicId)
            path = self.getPath(dic,musicId)
            if os.path.exists(path): return
            with open(path,'wb') as f:
                f.write(bytes(self._decrypt(cachePath)))
        except Exception as e:  # from file
            print(e)
            if not os.path.exists(idpath):
                with open(idpath,'wb') as f:
                    f.write(bytes(self._decrypt(cachePath)))
            dic = self.getInfoFromFile(idpath)
            path = getPath(dic,musicId)
            if os.path.exists(path):
                os.remove(idpath)
                return
            os.rename(idpath, path)

    def _decrypt(self,cachePath):
        with open(cachePath, 'rb') as f:
            btay = bytearray(f.read())
        for i, j in enumerate(btay):
            btay[i] = j ^ 0xa3
        return btay

    def getLyric(self, musicId):
        name = self.id_name[musicId]
        url = API + 'type=lyric&id=' + musicId
        url2 = 'https://music.163.com/api/song/lyric?id='+ musicId +'&lv=1&kv=1&tv=-1'
        try:
            lrc = requests.get(url).json()['lrc']['lyric']
            if lrc=='':
                lrc = requests.get(url2).json()['lrc']['lyric']
            if lrc=='':
                raise Exception('')
            file = os.path.join(LRCDIR, name + '.lrc')
            if not os.path.exists(file):
                with open(file, 'w', encoding='utf8') as f:
                    f.write(str(lrc))
        except Exception as e:
            pass
            #print(e,end='')
            #safeprint(': Failed to get lyric of music '+name)
    def getMusic(self):
        for ct, name in enumerate(self.files):
            self.decrypt(name)
            musicId = self.name_id[name]
            print('[{}]'.format(ct+1).ljust(5)+self.id_name[musicId])
            self.getLyric(musicId)


if __name__ == '__main__':
    platform = os.sys.platform.lower()
    user = getpass.getuser()
    path = ''
    if len(sys.argv) > 1:
        path = sys.argv[1].strip()
    elif os.path.exists(SRCDIR):
        path = SRCDIR
    elif platform.startswith('win'):
        path =  'C:/Users/{user}/AppData/Local/Netease/CloudMusic/Cache/Cache'.format(user= user)
    elif platform.startswith('linux'):
        pass # todo
    else:  # macpro
        path = '/Users/macbookpro({})/Library/Containers/com.netease.163music/Data/Caches/online_play_cache'.format(user = user)
    if not os.path.exists(path):
        raise Exception('Path not exists')
    if len(os.listdir(path))==0:
        raise Exception('No cache file found')
    else:
        path = os.path.abspath(path)
        handler = netease_music(path)
        handler.getMusic()
