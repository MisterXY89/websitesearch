
### [START] import ###
import requests
import tldextract
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer
### [END] import ###

# TODO: add console arg handler #
# TODO: add depth support		#

### [START] gloabl file config ###
DEPTH = 1  # currently not used
WORD = "Hotel"
URL = "https://www.sueddeutsche.de/"

URL_domain = tldextract.extract(URL).domain
URL_subdomain = tldextract.extract(URL).subdomain
URL_suffix = tldextract.extract(URL).suffix

urlList = []
### [END] global file config ###


"""
returns number of occurences of specifed word in URL
""" 
def countWords(url, word):	
	try:
		r = requests.get(url, allow_redirects=False)
		soup = BeautifulSoup(r.content, 'lxml')
		words = soup.findAll(text=lambda text: text and word in text)
		count  = 0		
		if words != None:
			for elt in words:
				count += elt.count(WORD) 
			print("Es wurde %s mal das Wort '%s' in der Url '%s' gefunden." %(count,word,url))
			return count
	except Exception as e:
		print(e)	
	return 0
 

"""
MAIN METHOD: "controller of program"
1. get all on the site pointing to TLD of domain the search is executed on
2. get number of occurnces of specified word in each URL
3. count all numbers up and return
"""
def main():
	urlList = getLinks(URL)
	count = 0
	for url in urlList:
		# find all URLS in url and appedn to urlListDepth2 and merge it with urlList ...		
		count += countWords(url, WORD)
	print("\n%s documents have been searched."%len(urlList))
	print('Url: %s\ncontains %s occurrences of word: %s'%(URL, count, WORD))


"""
Gets all links from given url
"""
def getLinks(url):	
	resp = requests.get(url)
	soup = BeautifulSoup(resp.content, 'lxml')
	for link in soup.find_all('a', href=True):
		tmp = link['href']
		print("Adding %s to urlList." %tmp)
		urlList.append(tmp)
	return verifyLinks(removeDuplicates(urlList))


"""
Removes all links to external sites from list
"""
def verifyLinks(urlList):
	print("Verifing urls")
	for i in range(len(urlList) - 1, -1, -1):
		url = urlList[i]
		tmpResult = tldextract.extract(url)
		tmpDomain = tmpResult.domain
		if tmpDomain == URL_domain and not url.__contains__("mailto:"):
			print("Url '%s' is okay."%url)
		elif tmpDomain == "php" or tmpDomain == "html":
			urlList[i] = ("%s%s"%(URL,url))
			print("Url wurde von '%s' in '%s' geändert." %(url, urlList[i]))
		else:
			print("Deleting %s from url list." %url)
			del urlList[i]
	return urlList


"""
Removing duplicates in lists
"""
def removeDuplicates(list_):
	return list(set(list_))


if __name__ == '__main__':
	main()