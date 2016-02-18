import pymongo
from bson.json_util import dumps
import time
import json
import requests
import os
import re
import datetime,elasticsearch
import threading
from bs4 import BeautifulSoup as bs
import sys
 
def insert(d):
    es=elasticsearch.Elasticsearch("192.168.101.5:9200")
    idd=d["id"]
    del d["id"]
    es.index(index="nutch",id=idd,doc_type="doc",body=d)
    print "INSERTED"
   
def cleanDom(html):
    soup=bs(html)
    removeTags=["script","style","noscript","img","form","input","iframe","header","footer","button","pre","br","code","select","option","nav"]
    for r in removeTags:
        try:
            dd=soup.findAll(r)
            for ddd in dd:
                ddd.decompose()
        except Exception as e:
            print e
    return soup
   
def removeNonAscii(data):
    return str(filter(lambda x:ord(x)>31 and ord(x)<128,data))
   
def removeUnEncoded(data):
    try:
        data=data.replace("\\n"," ")
        data=data.replace("\\r"," ")
        data=data.replace("\\t"," ")
        data=re.sub(r"(\\)(.*?)\s"," ",data)
        data=re.sub(r"\\(.*?)(\s|$)"," ",data)
        #Removing punctuations
        data=re.sub("&(.*?);"," ",data)#&nbsp; etc
        data=removeNonAscii(data)
        return re.sub("\s+"," ",data).strip()
    except:
        print "[ERROR] in removeUnEncoded"
       
def getId(url):
    try:
        k="/".join(url.split("/",3)[:3])
        host=k.replace("http://","").replace("https://","")
        host=host.split(".")[::-1]
        if url.replace(k,"")=="":
            if "https://" in url:
                c=".".join(host)+":https/"+url.replace(k,"")
            else:
                c=".".join(host)+":http/"+url.replace(k,"")
            return c
        if url.replace(k,"")[0]=="/":
            if "https://" in url:
                c=".".join(host)+":https/"+url.replace(k,"")[1:]
            else:
                c=".".join(host)+":http/"+url.replace(k,"")[1:]
        else:
            if "https://" in url:
                c=".".join(host)+":https/"+url.replace(k,"")
            else:
                c=".".join(host)+":http/"+url.replace(k,"")
        return c
    except:
        print "ERROR in getID"
       
def parse(url):
    print url
    html = requests.get(j).content
    isBody=False
    d={}
    soup=cleanDom(html)
    metas=soup.findAll("meta",{"name":["keywords","author"]})
    meta=[]
    for m in metas:
        meta+=removeUnEncoded(m.attrs["content"].lower()).replace(" ,",",").replace(", ",",").split(",")
    d["meta_keywords"]=meta
    d["host"]="/".join(url.split("/",3)[:3]).replace("http://","").replace("https://","")
   
    b=soup.find("body")
    if b is not None:
        isBody=True
        d["content"]=removeUnEncoded(b.text)
    else:
        d["content"]=""
   
    a=soup.find("title")
    if a is not None:
        d["title"]=removeUnEncoded(soup.find("title").text)
    else:
        d["title"]=""
 
 
    c=soup.find("meta",{"name":"description"})
    if not c is None:
        d["meta_description"]=removeUnEncoded(c.attrs["content"])
    else:
        if isBody:
            d["meta_description"]=d["content"][:400]
        else:
            d["meta_description"]=""
   
    d["url"]=url
    d["boost"]="0.0"
    d["id"]=getId(url)
    d["lastModified"]=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4]+"Z"
    d["digest"]=""
    d["tstamp"]=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4]+"Z"
    d["date"]=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4]+"Z"
    d["anchor"]=""
    d["cache"]="content"
    d["content_length"]=len(d["content"])
    d["commoncrawl"]="true"
    insert(d)
   
client = pymongo.MongoClient()
db = client['cron-dbpedia']
coll = db['external-links_en']
 
 
x=list(coll.find())
for i in range(len(x)):
    for j in x[i].get('to'):
        if threading.activeCount() < 500:
           
            try:
                threading.Thread(target = parse, args = (j,)).start()
                print "+++++++++++++++++++++++++++++"
            except Exception as e:
                print e
                print "---------------------------------------------------------"
        else:
            while True:
                if threading.activeCount() < 500:
                    break