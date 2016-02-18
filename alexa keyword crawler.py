import requests
from bs4 import BeautifulSoup as b
from pymongo import MongoClient
import time
from multiprocessing import Pool

url = "http://www.alexa.com/siteinfo/"
file = open("filtered-domains.txt",'r')
client = MongoClient(connect=False)
db = client.alexa
keyword = db.keyword

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

def soup(domain,link):
	try:
		tags = []
		table = domain.find("table",{"id":"keywords_top_keywords_table"}).find("tbody").findAll("td")
		for i in range(len(table)):
			if i%2 == 0:
				tags.append(table[i].findAll("span")[1].text.encode('utf-8'))
		put("found all tags of "+link,"INFO")
		return tags
	except Excption as e:
		put(e,"WARNING")

def main(line):
	try:
		tags = soup(b(requests.get((url+line).strip()).content,"lxml"),line)
		dic ={}
		dic[line.strip()] = tags
		put(dic,"SUCCESS")
		keyword.insert(dic, check_keys=False)
		put(line.strip()+" added to MongoClient","ENDC")
	except Exception as e:
		put(e,"FAIL")

if __name__ == "__main__":
	p = Pool(50)
	main(p.map(main, file))