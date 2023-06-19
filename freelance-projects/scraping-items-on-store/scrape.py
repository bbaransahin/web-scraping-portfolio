import requests
from bs4 import BeautifulSoup

init_link = 'https://www.vatanbilgisayar.com/apple/notebook/?page='
page_num = 1
items = {
        "name": [],
        "price": [],
        }

my_session = requests.Session()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
headers = {
        "User-Agent": user_agent,
        }

cookies = {
        "checkCookie": "true",
        "VLCV1OK": "1",
        "OfferMiner_ID": "EMJDFGSPFSWAQFEC20220211014316",
        "_gcl_au": "1.1.2111698855.1687156837",
        "_gaexp": "GAX1.2.8Mf-jzbCR1GDkBhbIB9_tA.19564.1",
        "_sgf_user_id": "6650576102711984129",
        "_sgf_session_id": "6650576102711984128",
        "_gid": "GA1.2.1934864860.1687156840",
        "ASP.NET_SessionId": "r3fjmecx0y40doqwhsneu0ju",
        "aid": "wdiwbjdcqjh1rgmcemczz40p",
        "__RequestVerificationToken": "bM4bpqaXZsmKo0Df9xXsO3v-RQh5KMyDV48fHIoIEQfyWa1FTAIHXVwVeQCanCCcNf44iFGEdOxa5bVuDrKWgLZBh-U1",
        "_sgf_exp": "",
        "_ga_5VWLM3S706": "GS1.1.1687156839.1.1.1687159431.58.0.0",
        "_ga": "GA1.2.1438705197.1644532992",
        }

def get_items(rawhtml):
    '''
    Collects the items with its features from a store page and adds them to items dictionary.
    Returns True if there is an item found, otherwise returns False.
    '''
    flag = False

    soup = BeautifulSoup(rawhtml, 'html.parser')
    soup_items = soup.find_all(class_='product-list')
    for soup_item in soup_items:
        new_item = []
        new_item.append(soup_item.find(class_='product-list__product-name').text)
        new_item.append(soup_item.find(class_='product-list__price').text)
        items['name'].append(new_item[0])
        items['price'].append(float(new_item[1]))
        flag = True
        print("new item found:\n"+new_item[0]+"\nprice:"+new_item[1])

    return flag

def scrape(page_num):
    print("scraping page num ", page_num)
    response = my_session.get(init_link+str(page_num), headers=headers, cookies = cookies)
    if(get_items(response.text)):
        scrape(page_num+1)

if __name__ == "__main__":
    scrape(page_num)
    print(items)
