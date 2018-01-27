from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from itertools import zip_longest
from collections import Iterable
from lxml import etree
from operator import or_
import sys
import requests 
import json
import glob
import re
import os


class netEaseMusic:
    def __init__(self,path=''):
        if path == '':path = input('input the path of  cached netease_music')
        self.path = path
        os.chdir(path)
        self.names=glob.glob('*.uc!')
        self.id_mp = {}
        for i in self.names:self.id_mp[self.getId(i)] = i
        self.absPaths=[os.path.abspath(i) for i in self.names]
        self.prep()
        self.headers={
            'Referer':'http://music.163.com/',
            'Host':'music.163.com',
            'Connection':'keep-alive',
            'User-Agent': 'ozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
        self.nameXpath ='//div[@class="tit"]/em[@class="f-ff2"]/text()'
        self.lrcSentencePt=re.compile(r'\[\d+:\d+.\d+\]([\w\d]+)\\n')         # wrong  (r'\[\d+,\d+\](\(\d+,\d+\)(\w))+\n')
        self.hasLrcPt= re.compile(r'(lyric|lrc|klyric|kalaokLyric|tlyric)\s*[\'\"]:\s*[\'\"]\s*\[')
        self.lrcKey = li = 'lyric|lrc|klyric|kalaokLyric|tlyric'.split('|')
    def prep(self):   
        self.prt= os.path.dirname(os.getcwd())
        self.cd('cached_网易云音乐')
        self.cd('cached_网易云音乐/lyric')
        self.cd('cached_网易云音乐/music')
        
    def cd(self,s):
        '''cd to the dir path+s, (create it first if not exists)'''
        try:
            os.chdir(self.prt)
            os.chdir(s)
        except:
            os.mkdir(s)
            os.chdir(s)
        
    def getId(self,name):
        if name[-1] not in '0987654321':
            name = os.path.basename(name)
        return name[:name.find('-')]
    def getIdFromIdx(self,idxFileName):
        with open(idxFileName,'r') as f:
            try:
                info = json.load(f)   #  r'\"musicId\":(\d+)'
            except:
                raise Exception('file {} is breaken'.format(idxFileName))
        return info['musicId']
    def crawlName(self,musicId):
        url = 'https://music.163.com/#/song?id='+str(musicId)
        r= requests.get(url,headers = self.headers)
        if r.status_code !=200:
            print(r.status_code)
            raise  Exception('crawl Name Failed! Bad Responde from '+url)
        sl = etree.HTML(r.text)
        try:
            return sl.xpath(self.nameXpath)[0]
        except:
            raise  Exception('not find music name of id : '+str(musicId))
    def crawlLrc(self,musicId):
        url = ('http://music.163.com/api/song/lyric?id=' + str(musicId) + '&lv=1&kv=1&tv=-1')
        try:
            return requests.get(url).text
        except:
            raise   Exception('crawl lyric Failed! Bad Responde from '+url)
    def lrcFromFile(self,musicId):
        self.cd('Lyric')
        ### 而直接字符串操作路径可能出错
        with open(str(musicId),'r',errors = 'ignore') as f:   
            try:
                s=''
                d=json.load(f,encoding='utf8')
                if  self.noLrc(d):return ''
                else:
                    for i in self.lrcKey:
                        if i in d and d[i]!='':s+= d[i]
            except:pass
            finally:return s
    def noLrc(self,s):
        '''judge if a dict or a string  has lyrics'''
        if isinstance(s,str):
            return self.hasLrcPt.search(s) is  None
        else:
            return not  reduce(or_,[i in s and s[i]!='' for i in self.lrcKey])   
    def getLyric(self,musicId):
        lrc = self.lrcFromFile(musicId)
        name = self.id_mp[musicId]
        if lrc =='':
            try:
                lrc = self.crawlLrc(musicId)
            except:
                print('fail to get lyric of music  '+name)
                return 
        lrc_lst = self.lrcSentencePt.findall(lrc)
        if lrc_lst==[]:return
        self.cd('cached_网易云音乐/lyric')
        with open(name +'.txt','w') as f:
            f.write(name+'\n\n')
            f.write('\n'.join(lrc_lst))
        return lrc_lst
    def getInfo(self,musicId):
        try:return self.getInfoFromMp3(musicId)
        except:
            try:
                with open(self.id_mp[musicId][:-3]+'idx') as f:
                    s = f.read()
                    name = re.findall(r'\[ti:(.*?)\]',s)[0]
                    singer  = re.findall(r'\[ar:(.*?)\]',lrc)[0]
                    return {'artist':singer,'title':name}
            except:return {}
                
    def getInfoFromMp3(self,musicPath):
        tag = MP3(musicPath,ID3 = EasyID3)
        return dict(tag)
    def _genFileName(self,dic):
        tmp = ''
        if 'title' in dic:  tmp =  '-'.join(dic['title'])
        if 'artist' in dic:  tmp+='--'+'-'.join(dic['artist'])
        if tmp =='--':
            try:tmp = self.crawlName()
            except Exception as e:
                print(repr(e))
                tmp = 'netease-music-'+musicId
        return tmp
    def decrypt(self,fileName):
        with open (fileName,'rb') as f:
            btay = bytearray(f.read())
        musicId = self.getId(fileName)
        self.cd('cached_网易云音乐/music')
        with open(str(musicId),'wb') as out:
            for i,j in enumerate(btay):
                btay[i] = j ^ 0xa3
            out.write(bytes(btay))
        dic = self.getInfo(musicId)
        newName = self.id_mp[musicId] =  self._genFileName(dic)
        if newName == '':newName = musicId
        try:os.rename(musicId,newName+'.mp3')
        except:pass
        return musicId
    def getMusic(self):
        for i in self.absPaths:
            musicId  = self.decrypt(i)
            self.getLyric(musicId)



path = sys.argv[1:][0].strip()
#path = 'C:\\Users\\mbinary\\Desktop\\source\\myscripts\\Music1'
hd = netEaseMusic(path)
hd.getMusic()
