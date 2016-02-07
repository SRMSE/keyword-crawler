import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
client = MongoClient()
db = client.test
similarsites = db.similarsites

url = "http://www.similarsites.com/browse"
soup = bs(requests.get(url).content,"lxml")
list = soup.find("ul",{"class":"pagination"}).findAll("a")
alphabet = []
for alphabet_link in list:
	alphabet.append("http://www.similarsites.com" + alphabet_link.get("href"))
#print alphabet

flag = 0
for current_alphabet in alphabet:
	print current_alphabet
	page = 1
	while True:
		try:
			current_alphabet_soup = bs(requests.get(current_alphabet+"/"+str(page)).content,"lxml")
			page += 1
			domains = current_alphabet_soup.find("tbody").findAll("a")
			for current_domain in domains:
				link = "http://www.similarsites.com" +current_domain.get("href")
				print link
				link_soup = bs(requests.get(link).content,"lxml")
				similar_topics = link_soup.find("section",{"id":"similarTopics"}).findAll("div",{"class":"row"})
				i=[]
				dic={}
				for topics in similar_topics:
					i.append(topics.text.split("'")[1].strip())
				dic["tags"]=i
				print dic
				dic.update({"link":link})
				similarsites.insert(dic)

			print page

		except Exception as e:
			flag += 1
			print e
		if flag == 5:
			break