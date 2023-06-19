import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import uuid

LINK_LIST_PATH = "link_list0.txt"

# Encoding for writing the URLs to the .txt file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"

init_link = 'https://www.gov.pl/web/diplomacy/news-'


def save_link(url, page):
    """
    Save collected link/url and page to the .txt file in LINK_LIST_PATH
    """
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    with open(LINK_LIST_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, url, str(page)]) + "\n")


def download_links_from_index(downloaded_url_list):
    """
    This function should go to the defined "url" and download the news page links from all
    pages and save them into a .txt file.
    """
    flag = False

    for downloaded_url in downloaded_url_list:
        response = requests.get(downloaded_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')

            for link in links:
                link = link.get('href')
                try:
                    if 'https' not in link:
                        link = downloaded_url_list[0] + link

                    if downloaded_url_list[0].split('/')[2] not in link:
                        continue

                    # Save the collected url in the variable "collected_url"
                    collected_url = link

                    if collected_url not in downloaded_url_list:
                        page = requests.get(link).status_code == 200
                        print("\t", collected_url, flush=True)
                        save_link(collected_url, page)
                        flag = True
                except Exception as e:
                    print(e, link)

    if len(downloaded_url_list) == 0:
        downloaded_url_list.append(init_link)
        page = requests.get(init_link).status_code == 200
        print("\t", init_link, flush=True)
        save_link(init_link, page)
        flag = True

    print('flag=', flag)
    if flag:
        download_links_from_index(downloaded_url_list)


def main():
    # Checking if the link_list.txt file exists
    if not os.path.exists(LINK_LIST_PATH):
        with open(LINK_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url", "page"]) + "\n")
        start_page = 1
        downloaded_url_list = []
    else:
        # Get the page to start from
        data = pd.read_csv(LINK_LIST_PATH, sep="\t")
        if data.shape[0] == 0:
            start_page = 1
            downloaded_url_list = []
        else:
            start_page = data["page"].astype("int").max()
            downloaded_url_list = data["url"].to_list()

    download_links_from_index(downloaded_url_list)


if __name__ == "__main__":
    main()
