#coding : utf-8
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
        self.lrcSentencePt=re.compile(r'\[\d+:\d+\.\d+\](.*?)\\n')         # wrong  (r'\[\d+,\d+\](\(\d+,\d+\)(\w))+\n')     
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
    def getInfo(self,musicId):
        try:return self.getInfoFromMp3(musicId)
        except:
            with open(musicId,'rb') as f:
                s = f.read().decode('utf8',errors ='ignore')
                dic = {}
                mch = re.findall(r'\[ar:(.*?)\]',s)
                #  to keep consistent with the id3 tag : namely the value is a list
                dic['artist']=mch[0] if  mch !=[] else ['']  
                mch = re.findall(r'\[ti:(.*?)\]',s)
                dic['title']=mch[0] if  mch !=[] else ['']
                return dic

    def _genFileName(self,dic,musicId):
        name = musicId
        if 'title' in dic:
            name =  dic['title'][0]
            if 'artist' in dic:  name+='--'+dic['artist'][0]
        else:
            try:name  = self.crawlName(musicId)
            except Exception as e:
                print(repr(e))
        return name
    
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
        newName = self.id_mp[musicId] =  self._genFileName(dic,musicId)
        if newName == '':newName = musicId
        try:os.rename(musicId,newName+'.mp3')
        except:pass
        return musicId
    
    def crawlName(self,musicId):
        url = 'https://music.163.com/#/song?id='+str(musicId)
        r= requests.get(url,headers = self.headers)
        if r.status_code !=200:
            print(r.status_code)
            raise  Exception('crawl Name Failed! Bad Responde from '+url)
        sl = etree.HTML(r.text)
        try:
            li = sl.xpath(self.nameXpath)[0]
            return '' if li ==[] else li[0]
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
        ### 直接字符串操作路径可能出错
        try:
            with open(str(musicId),'r') as f:   
                return  f.read()
        except:
            try:
                with open(str(musicId),'rb') as f:   
                    return  f.read().decode('utf8',errors = 'ignore')  # key point
            except:return self.crawlLrc(musicId)
    def getLyric(self,musicId):
        lrc = self.lrcFromFile(musicId)
        name = self.id_mp[musicId]
        lrc_lst = self.lrcSentencePt.findall(lrc)
        if lrc_lst==[]:
            try:
                lrc = self.crawlLrc(musicId)
                lrc_lst = self.lrcSentencePt.findall(lrc)
            except:
                print('fail to get lyric of music  '+name)
                return  
        self.cd('cached_网易云音乐/lyric')
        with open(name +'.txt','w',encoding ='utf8') as f:
            f.write(name+'\n\n')
            f.write('\n'.join(lrc_lst))
        return lrc_lst
    
                
    def getInfoFromMp3(self,musicPath):
        tag = MP3(musicPath,ID3 = EasyID3)
        return dict(tag)
    
    def getMusic(self):
        for i in self.absPaths:
            musicId  = self.decrypt(i)
            print(self.id_mp[musicId])
            self.getLyric(musicId)



path = sys.argv[1:][0].strip()
#path = 'C:\\Users\\mbinary\\Desktop\\source\\\\myscripts\\Music1'
hd = netEaseMusic(path)
hd.getMusic()

