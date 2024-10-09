import requests
import os
import paths
from lxml import html
import itertools
import re

ALLOW_DOWNLOAD: bool = True
TOPIC: str = "Sentiment analysis".replace(" ", "+")
NUMBER_OF_PAPERS: int = 1000

BASE_SIZE: int = 50

URL: str = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term="+str(TOPIC)+"&terms-0-field=abstract&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=hide&size="+str(BASE_SIZE)+"&order=-announced_date_first&start={start}"

def get_request(url) -> requests.Response:

    response = requests.get(url)

    if response.status_code == 200:
        arxiv = html.fromstring(response.content)

        if not arxiv.xpath('//title[contains(text(), "reCAPTCHA")]'):
            return response
    
    print("reCAPTCHA detected")
    return None


def collect_papers():
    papers_collected = 0
    current_page = 0

    while papers_collected < NUMBER_OF_PAPERS:
        response = get_request(URL.format(start=str(current_page * BASE_SIZE)))

        current_page += 1

        if (not(response) or response.status_code != 200):
            print(f"GET Request Failed for {current_page} page")
            return
            
        arxiv = html.fromstring(response.content)

        if arxiv.xpath('//title[contains(text(), "reCAPTCHA")]'):
            print("reCAPTCHA detected")
            exit()

        arxiv_papers_urls = arxiv.xpath('//*[@class="arxiv-result"]//p[contains(@class, "list-title")]/a/@href')
        
        if len(arxiv_papers_urls) == 0:
            print(f"No papers found on page {current_page}")
            break

        for url in arxiv_papers_urls:
            if try_download_paper(url):
                papers_collected += 1
                

def try_download_paper(url: str):
    url.replace("/abs/", "/html/")
    response = get_request(url)

    if (not(response) or response.status_code != 200):
        return False
    
    page = html.fromstring(response.content)
    if page.xpath('//main[@id="main-container"]//h1[contains(text(), "No HTML for")]'):
        return False
    
    if page.xpath('//title[contains(text(), "reCAPTCHA")]'):
        print("reCAPTCHA detected")
        return False
    
    paper_id = url.split("/")[-1]

    html_content = str(response.text)

    if ALLOW_DOWNLOAD:         
        with open(f"{paths.HTML_FOLDER}/{paper_id}.html", "w", encoding="utf-8") as file:
            file.write(html_content)    

    return True                                


if __name__ == "__main__":
    if not os.path.exists(paths.HTML_FOLDER):
        os.makedirs(paths.HTML_FOLDER)

    collect_papers()
