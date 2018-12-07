
### [START] import ###
import requests
import tldextract
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer
### [END] import ###


# TODO 1: add console arg handler #
# TODO 2: add depth support #
# TODO 3: add date filter (time datetime="2018-12-07 08:37:01" 
# class="timeformat">7. Dezember 2018, 08:37 Uhr</time>) from sz


### [START] gloabl file config ###
DEPTH = 2  # currently not used
WORD = "CDU"
URL = "https://www.startpage.com"
URL = "http://www.cipes.de/andrea"
URL = "https://www.uni-konstanz.de/"

URL_domain = tldextract.extract(URL).domain
URL_subdomain = tldextract.extract(URL).subdomain
URL_suffix = tldextract.extract(URL).suffix

urlList = []
whereFound = {}
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
			if count >= 1:
				whereFound.update({url:count})
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
	if DEPTH == 2:
		for url in urlList:
			# [todo 2] -> find all URLS in url and append to urlListDepth2
			# and merge it with urlList ... 
			tmpList = getLinks(url)
			urlList += tmpList
			urlList = removeDuplicates(urlList)

	for urlDepth in urlList:		
		count += countWords(urlDepth, WORD)
	print("\n%s documents have been searched."%len(urlList))
	print('Url: %s\ncontains %s occurrences of word: %s'%(URL, count, WORD))
	print(whereFound)


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
			urlList[i] = ("%s/%s"%(URL,url))
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