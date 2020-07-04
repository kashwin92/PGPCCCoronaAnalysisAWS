import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import datetime, time
import requests
import schedule

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def covid_extract():
    url = "https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide"    
	html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    lst = []
    for link in soup.findAll('a'):
        lnk = link.get('href')
        if lnk == None:
            continue
        else:
            if lnk[57:60] == "csv":
                lst.append(lnk)

    r = requests.get(lst[0], allow_redirects=True)
    open('covid19_data.txt', 'wb').write(r.content)

covid_extract()