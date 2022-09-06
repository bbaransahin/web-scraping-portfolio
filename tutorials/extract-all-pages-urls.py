import bs4
import requests

pages = [] # All of the visited pages are saving to this list
pages_visited = [] # Tracking to not to visit same page twice

def extract_all_page_urls(address):
    print(address)

    pages_visited.append(address)

    url = address
    hdr = {'User-Agent': 'Mozilla/5.0'} # To prevent 403 response
    req = requests.get(url, headers=hdr)
    soup = bs4.BeautifulSoup(req.text, "html.parser")
 
    # I was having problem while scraping so added a try except block to ignore pages that I have error
    # These are usually files, for example when it tries to find links inside of zip file it terminates the program
    try:
        if (soup.find_all('a') == None):
            return None;

        for link in soup.find_all('a'):
            if ((not link == None) and ('https://bilisimvadisi.com' in link.get('href'))):
                pages.append(link.get('href'))
                if (not link.get('href') in pages_visited):
                    extract_all_page_urls(link.get('href'))
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(address)
        print(e)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

extract_all_page_urls('https://bilisimvadisi.com.tr')

print("num pages:", len(pages))
print("num pages visited:", len(pages_visited))
