import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from time
client = MongoClient()
db = client.test
similarsites = db.similarsites
bcolors={
	"HEADER" : '\033[95m',
    "INFO" : '\033[94m',
    "SUCCESS" : '\033[92m',
    "WARNING" : '\033[93m',
    "FAIL" : '\033[91m',
    "ENDC" : '\033[0m',
    "BOLD" : '\033[1m',
    "UNDERLINE" : '\033[4m'
}

def put(msg,type):
	print bcolors[type.upper()] + ""+"["+time.asctime( time.localtime(time.time()) )+"]\t["+type.strip().capitalize()+"]\t"+str(msg)+"" + bcolors["ENDC"]

url = "http://www.similarsites.com/browse"
soup = bs(requests.get(url).content,"lxml")
list = soup.find("ul",{"class":"pagination"}).findAll("a")
alphabet = []
for alphabet_link in list:
	alphabet.append("http://www.similarsites.com" + alphabet_link.get("href"))
#print alphabet

flag = 0
for current_alphabet in alphabet:
	page = 1
	while True:
		try:
			current_alphabet_soup = bs(requests.get(current_alphabet+"/"+str(page)).content,"lxml")
			
			domains = current_alphabet_soup.find("tbody").findAll("a")
			
			for current_domain in domains:
				link = "http://www.similarsites.com" +current_domain.get("href")
				link_soup = bs(requests.get(link).content,"lxml")
				try:
					similar_topics = link_soup.find("section",{"id":"similarTopics"}).findAll("div",{"class":"row"})
					i=[]
					dic={}
					for topics in similar_topics:
						i.append(topics.text.split("'")[1].strip().encode('utf-8'))
					dic["tags"]=i
					
					dic.update({"link":link})
					#similarsites.insert(dic)
					put(dic,"SUCCESS")
					print current_alphabet
					print page
					print "-------------------------------------------------------------------"
				
				except Exception as e:
					put(e,"FAIL")
					continue
			page += 1
		except Exception as e:
			flag += 1
			print e
		if flag == 5:
			break