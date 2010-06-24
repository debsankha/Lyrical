#! /usr/bin/python
#############################################################
# This scripts fetches lyrics of the song currently    
# playing in amarok by means of a simple google search.
# Remember that it depends on the <title> and <artist> 
# tag of the audio file to fetch lyrics. So if this    
# script doesn't work for you, first try changing them 
# appropriately.	       			       
#############################################################

# TO CHANGE:
# What abt stupid php/javascript rendered lyrics????
# ? add the tentative cluster item (the 1st item)?? It eliminates the unnecessary titles. added it. disallowing any other tag eliminates that possibility.
# But that creates problems with <p> tags within genuine lyrics.

from commands import getoutput as get
from search import GoogleSearch
from urllib import urlopen
import os
import user
import re

amarokid=get('dcop | grep amarok')

from getlyric import xmlcorrect,ascii_to_char,bylength,getlyric

def main():
	artist=get('dcop %s player artist'%amarokid).strip()
	title=get('dcop %s player title'%amarokid).strip()

	if title =='':
		searchstr=get('dcop %s player nowPlaying'%amarokid)+' lyrics'
	else :
		searchstr='''"'''+title+'''"'''+' '+artist+' lyrics'

	gs=GoogleSearch(searchstr)
	print 'Googling for ',searchstr
	gs.results_per_page=10
	try:
		results=gs.get_results()
	except:
		os.popen("dcop %s contextbrowser showLyrics '<lyric>Google.com is not accessible. Check your internet connection and retry</lyric>'"%amarokid)
		print 'google.com is not accessible'
		return ''

	xml=open('%s/tmp.xml'%user.home,'w')
	for res in results:
		lyric=getlyric(res.url.encode('utf8'),title)
		if lyric=='':
			pass
		else :
			print 'the lyric is:\n%s'%lyric
			xmldoc=xmlcorrect(lyric)
			xmldoc="""<lyric artist="%s" title="%s" page_url="%s" >"""%(artist,title,res.url.encode('utf8'))+xmldoc+'</lyric>'
			print >> xml, xmldoc
			xml.close()
			sh=open('%s/tmp.sh'%user.home,'w')
			print >> sh, "xml=$(cat ~/tmp.xml)"
			print >> sh, '''dcop %s contextbrowser showLyrics "${xml}"'''%amarokid
			sh.close()
			get("sh %s/tmp.sh"%user.home)
			break
		

main()
while True:
	if raw_input()=="trackChange":
		main()

