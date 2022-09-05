import bs4
import requests
import pickle

pages = []
pages_visited = []

def extract_all_page_urls(address):
    print(address)

    save_file = open("save.pkl","wb")
    pages_visited.append(address)
    pickle.dump(pages_visited, save_file)

    url = address
    hdr = {'User-Agent': 'Mozilla/5.0'} # To prevent 403 response
    req = requests.get(url, headers=hdr)
    soup = bs4.BeautifulSoup(req.text, "html.parser")

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

print("=============================RESULTS=============================")
for link in pages:
    print(link)

print("num pages:", len(pages))
print("num pages visited:", len(pages_visited))
