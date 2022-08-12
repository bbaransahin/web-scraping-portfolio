import bs4
import requests

url = "https://bilisimvadisi.com.tr/en/"
hdr = {'User-Agent': 'Mozilla/5.0'} # To prevent 403 response
req = requests.get(url, headers=hdr)
soup = bs4.BeautifulSoup(req.text, "html.parser")

print(soup.title) # No need to print the title but this proves that we get the page correctly

for link in soup.find_all('a'):
    if ((not link.get('href') == None) and ('http' in link.get('href'))): # To ignore mails, Nones etc.
        print(link.get('href'))
