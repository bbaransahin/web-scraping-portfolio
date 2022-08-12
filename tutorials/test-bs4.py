import bs4
import requests

url = "https://www.tutorialspoint.com/index.htm"
req = requests.get(url)
soup = bs4.BeautifulSoup(req.text, "html.parser")
print(soup.title)
