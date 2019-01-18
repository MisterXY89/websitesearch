# Website Word  Search
A litte program written in python.
Searches for a word in given URL. Finds all links of given URL and searches for given word in all URLS.

## Doc
I will explain some methods, some are obvious.
### General
At the top of `main.py` you can specify the `URL`,`WORD` and `DEPTH`. Currently only depth 1-2 is supported. If `DEPTH=2`, the program gets all URLS of the found URLS in the STARTURL. 
``` 
URL -> [foundUrls1] 
       [foundUrls1]  -> for each url in [foundUrls1] -> [foundUrls2]
[urlsCollection] = [foundUrls1] + [foundUrls2]

for each url in [urlsCollection] -> search for WORD
```
### `main()`
MAIN METHOD: "controller of program"
1. get all on the site pointing to TLD of domain the search is executed on
2. get number of occurnces of specified word in each URL
3. count all numbers up and return

###  `verifyLinks(urlList)`
Removes all links to external sites from list
Removes all mailTo link
Convert relativ url to absolute
Removes .jpg and .pdf files

## Requirements
I set up a python venv.
```bash
$ pip freeze
beautifulsoup4==4.7.1
certifi==2018.11.29
chardet==3.0.4
idna==2.8
lxml==4.3.0
pkg-resources==0.0.0
requests==2.21.0
requests-file==1.4.3
six==1.12.0
soupsieve==1.7.1
tldextract==2.2.0
urllib3==1.24.1
```

## Todos
 TODO 1: add console arg handler 
 TODO 2: adddepth support 
 TODO 3: add date filter (time datetime="2018-12-07 08:37:01" .timeformat




