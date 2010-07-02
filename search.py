import urllib,simplejson

class AppURLopener(urllib.FancyURLopener):
	version="""Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/6.0.437.3 Safari/534.1"""

class GoogleSearch:
	def __init__(self,phrase):
		self.searchstr=phrase
		self.results_per_page=10	#of no use now
	
	def get_results(self):
		query = urllib.urlencode([('q',self.searchstr)])
		url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s"%query
		urllib._urlopener = AppURLopener()
		search_results = urllib.urlopen(url)
		json = simplejson.loads(search_results.read())
		
		results=[]
		for res in json['responseData']['results']:
			results.append(res['url'])

		return results


