import bs4
import requests_html

def get_comments(address):
    comments = []

    session = requests_html.HTMLSession()
    print('session started')

    url = address
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = session.get(url, headers=hdr)
    print('got the url')
    req.html.render(sleep = 2, timeout = 30)
    print('rendered')

    soup = bs4.BeautifulSoup(req.text, 'lxml')

    print(soup.get_text())

    for item in soup.find_all('yt-formatted-string'):
        print("an item found")
        if (item.has_attr('class')):
            if(len(item['class']) != 0):
                if('ytd-comment-renderer' in item['class']):
                    print("==============================")
                    print(item.get_text())
                    print("==============================")

get_comments('https://www.youtube.com/watch?v=CvJ6Ic3PS7M&ab_channel=AryanSharma')
