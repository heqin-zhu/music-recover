#coding : utf-8
import os
import sys
import glob
import requests 

DESDIR = '../cached_网易云音乐'
LRCDIR = os.path.join(DESDIR,'lyric')
MSCDIR = os.path.join(DESDIR,'music')

API = 'https://api.imjad.cn/cloudmusic/?'
# two args: id  type
# type=song, lyric, comments, detail, artist, album, search
# eg  API = 'https://api.imjad.cn/cloudmusic/?type=song&id=1234132'    download music

hasModu = False
try:
    from mutagen.easyid3 import EasyID3
    from mutagen.mp3 import MP3
    hasModu = True
except:pass

class netease_music:
    def __init__(self,path=''):
        '''path is the direcoty that contains Music files(cached)'''
        if path == '': path = input('input the path of  cached netease_music')
        self.path = path
        os.chdir(path)
        self.files=glob.glob('*.uc!')
        self.id_mp = {}
        for i in self.files:self.id_mp[self.getId(i)] = i
        if not os.path.exists(DESDIR):os.mkdir(DESDIR)
        if not os.path.exists(LRCDIR):os.mkdir(LRCDIR)
        if not os.path.exists(MSCDIR):os.mkdir(MSCDIR)
        # import re
        # self.nameXpath ='//div[@class="tit"]/em[@class="f-ff2"]/text()'
        # self.lrcSentencePt=re.compile(r'\[\d+:\d+\.\d+\](.*?)\\n')         # wrong  (r'\[\d+,\d+\](\(\d+,\d+\)(\w))+\n')      
                
    def getId(self,name):
        return name[:name.find('-')]

    def getInfoFromWeb(self,musicId):
        dic = {}
        url = API+'type=detail&id=' + str(musicId)
        info = requests.get(url).json()['songs'][0]
        dic['artist']= [ info['ar'][0]['name']  ]
        dic['title']=  [ info['al']['name']     ]
        dic['cover'] = [ info['al']['picUrl']   ]
        return dic
    
    def getInfoFromFile(self,path):
        if not os.path.exists(path):
            print('Can not find file '+path)
            return {}
        elif hasModu:
            return dict(MP3(path,ID3 = EasyID3))
        else: 
            print('[Error ] You can use pip3 to install mutagen or connet to the Internet')
            raise Exception('Failed to get info of '+path)

    def genName(self,dic):         
        title = dic['title'][0]
        artist = dic['artist'][0]
        if artist in title: title = title.replace(artist,'').strip()
        return title + '--' + artist
        
    def decrypt(self,fileName):
        with open (fileName,'rb') as f:
            btay = bytearray(f.read())
        musicId = self.getId(fileName)
        idpath = os.path.join(MSCDIR,musicId)
        if not os.path.exists(idpath):
            with open(idpath,'wb') as out:
                for i,j in enumerate(btay):
                    btay[i] = j ^ 0xa3
                out.write(bytes(btay))
        dic = {}
        try:
            dic = self.getInfoFromWeb(musicId)
        except Exception as e:
            print(e)
            print('正在尝试获取 MP3 文件的元数据 ')
            dic = self.getInfoFromFile(os.path.join(MSCDIR,musicId))
        name = self.genName(dic)
        self.id_mp [musicId] = name
        path = os.path.join(MSCDIR,name+'.mp3')
        if os.path.exists(idpath) and not os.path.exists(path):
            os.rename(idpath,path)
        return musicId
    
    def getLyric(self,musicId):
        name = self.id_mp[musicId]
        # 'http://music.163.com/api/song/lyric?id='
        url = API+'type=lyric&id=' + str(musicId)
        try:
            lrc = requests.get(url).json()
            file = os.path.join(LRCDIR,name +'.lrc')
            if not os.path.exists(file):
                with open(file,'w',encoding ='utf8') as f:
                    f.write(str(lrc))
        except Exception as e:
            print(e,' Failed to get lyric of music '+name)
    
    def getMusic(self):
        for ct,i in enumerate(self.files):
            musicId  = self.decrypt(i)
            print('[Music {}]'.format(ct+1).ljust(12)+self.id_mp[musicId])
            self.getLyric(musicId)


if __name__=='__main__':
	if len(sys.argv) > 1: path = sys.argv[1].strip()
	else : path = os.path.join(os.getcwd(),'Music1')
	handler= netease_music(path)
	handler.getMusic()

