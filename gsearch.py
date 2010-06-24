import urllib
from BeautifulSoup import BeautifulSoup as soup
import re
from commands import getoutput as get

def gsearch(url):
	page=soup(f)
	print page
	search_results=page.find('div',id='res')
	lyriclinks=[]
	for i in search_results.findAll('a'):
		text=[str(part) for part in i.fetchText()]
		fulltext=''.join(text)
		if fulltext.count('<em>')>0:
			lyriclinks.append(str(i['href']))

	return lyriclinks


for i in gsearch('''http://www.google.com/search?hl=en&q="Wonderful+Day"+Elvis+Presley+lyrics+-search&aq=f&aqi=&aql=&oq=&gs_rfai='''):
	print i


