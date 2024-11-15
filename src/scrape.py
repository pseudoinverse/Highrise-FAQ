"""
Scrape the Highrise FAQ page to get all the FAQ content and save it to a JSON file
"""
import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://support.highrise.game/en/"
JSON_FILE_PATH = "../data/faq.json"

def get_collections():
    """
    Get all the collections from the FAQ page
    :return: Collection URLs as a list
    """
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    faq_collections = set()
    collections_url = BASE_URL + 'collections/'
    for a_tag in soup.select('a.collection-link'):
        link = a_tag['href']
        if link.startswith(collections_url):
            faq_collections.add(link)
    return list(faq_collections)


def get_faq_links():
    """
    Get all the FAQ links from the collections
    :return: FAQ links as a list
    """
    collections = get_collections()
    links = set()
    article_url = BASE_URL + 'articles/'

    for collection in collections:
        soup = BeautifulSoup(requests.get(collection).text, 'html.parser')
        for a_tag in soup.select('a.duration-250'):
            link = a_tag['href']
            if link.startswith(article_url):
                links.add(link)
    return list(links)

def scrape_faq_content():
    """
    Scrape content of the FAQ and save it to JSON file
    """
    faq_links = get_faq_links()
    faq_content = []
    for link in faq_links:
        soup = BeautifulSoup(requests.get(link).text, 'html.parser')
        title = soup.select_one('div.article header.font-primary').get_text()
        content = soup.select_one('article').get_text()
        content = content.split('Related Articles')[0] # Remove all text after related articles
        faq_content.append({'Link': link, 'Title': title, 'Content': content})

    with open(JSON_FILE_PATH, 'w') as json_file:
        json.dump(faq_content, json_file, indent=4)


def read_faq_json():
    """
    Read the FAQ JSON file and return the content
    :return: FAQ content as a map
    """
    with open(JSON_FILE_PATH) as json_file:
        faq_content = json.load(json_file)
    return faq_content


if __name__ == '__main__':
    scrape_faq_content()
