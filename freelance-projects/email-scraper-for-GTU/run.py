import requests
import re
from bs4 import BeautifulSoup

print('Getting main page..')
url = 'https://www.gtu.edu.tr/kategori/4/3/display.aspx'
response = requests.get(url)
soup=BeautifulSoup(response.text, 'html.parser')

# Find every link that points to academic personels page

# div id='main-content'
# initial link=https://www.gtu.edu.tr/kategori/4/3/display.aspx

print('Collecting necessary pages..')
soup = soup.find('div', {'id': 'main-content'})
allLinkObjs = soup.find_all('a')
allLinksDepartments = []
for linkObj in allLinkObjs:
    if (not (linkObj.get('href').startswith('http') or linkObj.get('href').startswith('www'))):
        allLinksDepartments.append('https://www.gtu.edu.tr/'+linkObj.get('href'))
    else:
        allLinksDepartments.append(linkObj.get('href'))

allLinks = []
for link in allLinksDepartments:
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup = soup.find('div', {'id': 'sidebar-first'})
        links = soup.find_all('a')
        for l in links:
            if ('Akademik Kadro' in l.text):
                allLinks.append(l.get('href'))
    except Exception as e:
        print('Error at page: '+link)
        print(e)

# Build a scraper function for these pages

def findMails(soup):
    mails = []
    divs = soup.find_all('div')
    for d in divs:
        if ('E-posta:' in d.text):
            wordsList = d.text.split()
            mails.append(wordsList[wordsList.index('E-posta:')+1])
    return mails

print('Scraping mails..')
mails = []
for link in allLinks:
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        for mail in findMails(soup):
            if ('gtu.edu.tr' in mail):
                mail = mail[:-10]+'@'+mail[-10:]
            if (not mail in mails):
                mails.append(mail)
    except Exception as e:
        print(e)

output_file = open('Output.txt', 'w+')

for mail in mails:
    output_file.write(mail+'\n')

output_file.close()

print('DONE')
