import os
from commands import getoutput as get
from search import GoogleSearch
from urllib import urlopen
import user
import re

def xmlcorrect(page):
	'''replacing invalid xml characters'''
	page=re.sub('&','&amp;',page)
	page=re.sub('<br[^>]*>|<BR[^>]*>',"&#xA;",page)
	page=re.sub("'",' ',page)
	page=re.sub('''"''',' ',page)
	page=re.sub('<','&lt;',page)
	page=re.sub(">",'&gt;',page)
	return page		

def ascii_to_char(match):
	'''For pages with lyric in ascii. returns corresponding char if arg<255 '''
	asc=int(match.group(2))
	if asc<256:
		return chr(asc)
	else :
		return '&#'+str(asc)

def bylength(str1,str2):
	'''for sorting a list w.r.t length of elements'''
	return len(str1)-len(str(2))

def getlyric(url):
	print 'looking for lyric in ',url
	try:
		f=urlopen(url)
		print 'Opened the url'
	except :
		print 'The website is not accessible'
		return '<lyric>The website could not be accessed. Check your internet connection and retry</lyric>'

	print "reading page"
	page=f.read()
	print "read the page"
	pre_tags=re.findall("(<pre>|<PRE>)([^<]*)(</pre>|</PRE>)",page)
	if pre_tags!=[]:
		print "got pre tags"
		contents=[tag[1] for tag in pre_tags]
		contents.sort(cmp=bylength)
		if (contents[-1]).count('\n')>7:
			return contents[-1]
		else :
			print "contents of pre tag is too low"
			pass
	else :
		print "No pre tag found"
		pass
		
	print "reverting to normal method"	
	page=re.sub("\s{3,}",' ',page)
	page=re.sub('<br[^>]*>|<BR[^>]*>',"<br>",page)
	page=re.sub('(<br>\s*){3,}',"<br><br>",page)
	page=re.sub("(&#)([0-9]*);?",ascii_to_char,page)
	page2=page
	brlist=[]
	difflist=[]
	omitted=0
	iscluster=0
	ly=[]
	while len(page)>=0:
		loc=page.find('<br')
		difflist.append(loc)
		if loc!=-1:
			if re.search("<(?!(br|p|/p))[^>]*>",page[:loc-1])!=None:
				tentative=omitted+loc
				page=page[loc+3:]
				omitted+=loc+3
				iscluster=0
			elif loc<=150 and iscluster==0:
				iscluster=1
				try:
					ly.append([tentative,omitted+loc])
				except:
					ly.append([omitted+loc])
				
				brlist.append(omitted+loc)
				page=page[loc+3:]
				omitted+=loc+3
			elif loc<=150 and iscluster==1:
				try:
					ly[len(ly)-1].append(tentative)
				except:
					pass

				ly[len(ly)-1].append(omitted+loc)
				brlist.append(omitted+loc)
				page=page[loc+3:]
				omitted+=loc+3
			elif loc>150 and iscluster==1:
				tentative=omitted+loc
				page=page[loc+3:]
				omitted+=loc+3
				iscluster=0
			elif loc>150 and iscluster==0:
				tentative=omitted+loc
				page=page[loc+3:]
				omitted+=loc+3
			else :
				pass
		
		else :
			break
	
	lenly=[len(i) for i in ly]
	if len(lenly)>0:
		if max(lenly)>=7:
			biggest_cluster=ly[lenly.index(max(lenly))]
			start=page2.rfind('>',0,biggest_cluster[0])
			end=page2.find('<',biggest_cluster[-1]+1,len(page2))
			lyric=page2[start+1:end]
			return lyric
		else :
			print "max(lenly)<7, most probably not a lyric. exiting.."
			return ''

	else :
		return ''


