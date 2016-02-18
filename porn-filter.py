import requests
import json
from bs4 import BeautifulSoup as b
import csv
import time
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
file = open("test.txt",'a')
#stopped at line 26576
i=0
reader= open('top-1m.csv','rb')

line=reader.readlines()
while True:
	domain = "http://api.mywot.com/0.4/public_link_json2?hosts=" + line[i].split(",")[1].strip() + "/&callback=process&key=2cad1d03acb160bd3b2ed67b8b8a2e7b96781f45"
	#print domain
	domain_soup = b(requests.get(domain).content,"lxml").find("body").text
	
	put(line[i].split(",")[1].strip()+ " at line " + str([i+1]), "INFO")
	json_data = json.loads(domain_soup.split("process(")[1].split(")")[0])
	try:
		json_data = json_data[json_data.keys()[0]]['categories'].keys()
		
		if ('401' in json_data) or ('402' in json_data):
			put("ADULT!!!!!!!", "WARNING")
			print "---------------------------------------------------------------------"
			
		else:
			put("SAFE FOR WORK", "SUCCESS")
			file.write(line[i].split(",")[1].strip()+"\n")
			print "------------------------------------------------------------------------"

	except Exception as e:
		put("DOES NOT CONTAIN INFO", "FAIL")
		print "------------------------------------------------------------------------------------"
	i += 1