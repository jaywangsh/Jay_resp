# -*- coding:utf-8 -*-  
import requests
from bs4 import BeautifulSoup
import io
import sys
import pymysql.cursors

#2017-06-17 爬所有网易云歌手
#1.pymysql中设置DEFAULT_CHARSET = 'utf-8'
#2.mysql中设置my.ini的character-set-server=utf8
#3.set character_set_client=gbk

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')#改变控制台输出的默认编码

connection = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         db='test',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
      
def save_artist(id,initial):
    #print("start save_artist")
    params = {'id': id, 'initial': initial}
    r = requests.get('http://music.163.com/discover/artist/cat',params=params)#爬网页
    type_map={1001:'华语男歌手',1002:'华语女歌手',1003:'华语组合'}
    
    soup = BeautifulSoup(r.content.decode(),'html.parser')
    body = soup.body
    hot_artists = body.find_all('a', attrs={'class': 'msk'})
    artists = body.find_all('a', attrs={'class': 'nm nm-icn f-thide s-fc0'})

    for hot_artist in hot_artists:
        artist_id = hot_artist['href'].replace('/artist?id=','').strip()
        artist_name_title=hot_artist['title']
        artist_name = artist_name_title[:len(artist_name_title)-3].strip()

        try:
            insert_db(artist_id,artist_name,type_map[id])
            #insert_db(artist_id,artist_name)
        except Exception as e:
            print(e)
       
    for artist in artists:
        artist_id = artist['href'].replace('/artist?id=','').strip()
        artist_name_title=artist['title']
        artist_name = artist_name_title[:len(artist_name_title)-3].strip() 

        try:
            insert_db(artist_id,artist_name,type_map[id])
            #insert_db(artist_id,artist_name)
        except Exception as e:
            print(e)
    #print("end save_artist")         


def insert_db(artist_id,artist_name,type):
    with connection.cursor() as cursor:
        sql="Insert into artist (ARTIST_ID, ARTIST_NAME,TYPE) VALUES (%s, %s, %s)"
        cursor.execute(sql,(artist_id,artist_name,type))
        #sql="Insert into artist (ARTIST_ID, ARTIST_NAME) VALUES (%s, %s)"
        #cursor.execute(sql,(artist_id,artist_name,type))
        connection.commit()


gid = [1001,1002,1003]

for i in gid:
    save_artist(i,0)#其他页
    for j in range(65,91):
        save_artist(gid,j)



