import os
import json
from bs4 import BeautifulSoup as bs
import pandas as pd

RAW_HTML_DIR = "rawhtmls"
PARSED_HTML_PATH = "parsedhtmls"

# Encoding for writing the parsed data to JSONS file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"


def extract_content_from_page(file_path):
    """
    This function should take as an input the path to one html file
    and return a dictionary "parsed_data" having the following information:

    parsed_data = {
        "date": Date of the news on the html page
        "title": Title of the news on the html page
        "content": The text content of the html page
        }

    This function is used in the parse_html_pages() function.
    You do not need to modify anything in that function.
    """
    parsed_data = {}

    with open(file_path) as file:
        html_doc = file.read()
    soup = bs(html_doc, 'html.parser')

    parsed_data['date'] = soup.find(class_='event-date').text
    parsed_data['title'] = soup.find('article').find('h2').text
    parsed_data['content'] = soup.find(class_='editor-content').text

    return parsed_data


def parse_html_pages():
    # Load the parsed pages
    parsed_id_set = set()
    if os.path.exists(PARSED_HTML_PATH):
        with open(PARSED_HTML_PATH, "r", encoding=ENCODING) as f:
            # Saving the parsed ids to avoid reparsing them
            for line in f:
                data = json.loads(line.strip())
                id_str = data["id"]
                parsed_id_set.add(id_str)
    else:
        with open(PARSED_HTML_PATH, "w", encoding=ENCODING) as f:
            pass

    # Iterating through html files
    for file_name in os.listdir(RAW_HTML_DIR):
        page_id = file_name[:-5]

        # Skip if already parsed
        if page_id in parsed_id_set:
            continue

        # Read the html file and extract the required information

        # Path to the html file
        file_path = os.path.join(RAW_HTML_DIR, file_name)

        try:
            parsed_data = extract_content_from_page(file_path)
            parsed_data["id"] = page_id
            print(f"Parsed page {page_id}")

            # Saving the parsed data
            with open(PARSED_HTML_PATH, "a", encoding=ENCODING) as f:
                f.write(json.dumps(parsed_data) + "\n")

        except Exception as e:
            print(f"Failed to parse page {page_id}: {e}")


if __name__ == "__main__":
    parse_html_pages()

