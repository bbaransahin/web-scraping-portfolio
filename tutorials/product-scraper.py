import bs4
import requests

class Product:
    def __init__ (self, name, artist, price):
        self.name = name
        self.artist = artist
        self.price = price
    def print (self):
        print('name: ', self.name)
        print('artist:', self.artist)
        print('price:', self.price, '\n')

def get_page (url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = requests.get(url, headers=hdr)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    return soup

def get_products (soup_obj):
    prds = []

    name_objs = soup_obj.find_all('a', {'class': 'prd-name'})
    artist_objs = soup_obj.find_all('a', {'class': 'who text-overflow'})
    price_objs = soup_obj.find_all('div', {'class': 'prd-price'})

    for i in range(len(name_objs)):
        temp_prd = Product(name_objs[i].text, artist_objs[i].text, price_objs[i].text)
        prds.append(temp_prd)

    return prds

products = []

page1 = get_page('https://www.dr.com.tr/kategori/Muzik/Yabanci-Albumler/Rock-Music/grupno=00708?Page=1')
page2 = get_page('https://www.dr.com.tr/kategori/Muzik/Yabanci-Albumler/Rock-Music/grupno=00708?Page=2')

products_buffer = get_products(page1)

for i in products_buffer:
    products.append(i)

products = get_products(page2)

for i in products_buffer:
    products.append(i)

for i in products:
    i.print()

print('Total products=', len(products))
