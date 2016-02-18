import requests
from bs4 import BeautifulSoup as b
url = "http://www.alexa.com/siteinfo/"
file = open("filtered-domains.txt",'r')
def soup(domain):
	tags = []
	table = domain.find("table",{"id":"keywords_top_keywords_table"}).find("tbody").findAll("td")
	for i in range(len(table)):
		if i%2 == 0:
			tags.append(table[i].findAll("span")[1].text.encode('utf-8'))
	return tags
	

for line in file:
#	print line
	tags = soup(b(requests.get((url+line).strip()).content,"lxml"))
	dic ={}
	dic[line.strip()] = tags
	print dic
