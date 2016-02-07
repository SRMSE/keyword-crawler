import requests
import json
from bs4 import BeautifulSoup as b
import csv
file = open("adult.txt",'a')
i=1
with open('top-1m.csv','rb') as f:
	reader = csv.reader(f)
	for row in reader:
		
		domain =  row[1]
		print str(i)+"\t\t"+domain
		link="http://api.mywot.com/0.4/public_link_json2?hosts="+(domain)+"/&callback=process&key=2cad1d03acb160bd3b2ed67b8b8a2e7b96781f45"
		print link
		domain_soup = b(requests.get(link).content,"lxml").find("body").text
		json_data = domain_soup.split("process(")[1].split(")")[0]
		json_data = json.loads(json_data)
		try:	
			json_data = json_data[json_data.keys()[0]]['categories'].keys()
			print json_data
			if ('401' in json_data) or ('402' in json_data):
				print "ADULT!!!!!!!"
				file.write(domain+"\n")
			else:
				print "------------------------"
		except Exception as e:
			print e
			file.write(domain+"\t\t"+"not indexed\n")
		i+=1