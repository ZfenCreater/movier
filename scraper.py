# -*- coding: utf-8 -*-

import urllib, urllib2, base64, sys, os, json
import re
import parsers


FF_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
HEADERS = {"User-Agent":FF_USER_AGENT}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Accept': '*/*',
            'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest'}

module=parsers.modules()

parser=parsers.vod_parsers
parser=parser().get_parsed_link
#@parts or @start @category @film

getlist=module.get_list

def realgetlist(url):
    global getlist, parser
    content=getlist(url)
    if "@start" in url or "@category" in url or "@film" in url:
        for trm in range(len(content)): 
            name_s = content[trm][1]
            url_s = content[trm][5]
            if content[trm][7] == None:
                pic = ''
            else:
                pic = content[trm][7]
            if content[trm][2] == None:
                description = ''
            else:
                description = content[trm][2]
            return url_s    
    if "@parts" in url: 
        for trm in range(len(content)):
            mode = 2
            name_p = content[trm][1]
            url_p = content[trm][4]
            if url_p == None :
                url_p = content[trm][5]
                mode = 1
            if content[trm][7] == None:
                pic = ''
            else:
                pic = content[trm][7]
            if content[trm][2] == None:
                description = ''
            else:
                description = content[trm][2]
            return url_p

def getreq(url):
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    html = response.read()
    return html

def download(url,file):
    req = urllib2.Request(url, None)
    response =urllib2.urlopen(req)
    try:
        filename=response.info()['Content-Disposition']
    except:
        filename=file
    html = response.read()
    with open(filename,"wb") as f:
        f.write(html)



def fullhdfilmizlesene():
    turl=url+"@parts@msa"
    lurl= parser(realgetlist(turl))
    return getreq(lurl)

def hdpizle(url):
    #720pizle
    turl=url+"@parts@msa"
    lurl= parser(realgetlist(turl))
    return (lurl)

def hdfilmcehennemi():
    turl=url+"@parts@ARES"
    lurl= (realgetlist(turl))
    return (lurl)


def search_hdpizle(url):
	url=url.replace(" ","%20")
	url="https://720pizle.org/?s="+url
	print(url)

	film_url = []
	film_name = []
	search = getreq(url)
	xx=1	
	while True:

		try:
			t_1=search.split('<a class="sayfa-icerik-baslik" href="')[xx].split('</a>')[0].split('"')[0]
			film_url.append(t_1)
			t_2=search.split('<a class="sayfa-icerik-baslik" href="')[xx].split('</a>')[0].split('>')[1].replace(" izle","")
			film_name.append(t_2)
		except:
			break
		xx+=2
	return(film_name,film_url)

url = (raw_input("aranacak film : "))

searched = search_hdpizle(url)
searched=searched[1][0]

download(hdpizle(searched)[1][1],"video.mp4")
