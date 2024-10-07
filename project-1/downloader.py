import requests
import os
import paths
from lxml import html

TOPIC = "cs.AI"
NUMBER_OF_PAPERS = 750
ALLOW_DOWNLOAD = False

URL = f"https://arxiv.org/list/{TOPIC}/recent?skip=0&show={NUMBER_OF_PAPERS}"

response = requests.get(URL)

print("GET Response Status Code:", response.status_code)
if (response.status_code != 200):
    print("GET Request Failed")
    exit()

arxiv = html.fromstring(response.content)

paper_anchor_tags = arxiv.xpath('//*[@id="articles"]//dt//a[text()="html"]')
print(f"Found {len(paper_anchor_tags)} papers (with html format) to download")

for anchor in paper_anchor_tags:
    url: str = anchor.xpath("@href")[0]
    id: str = anchor.xpath("@id")[0]

    # remove the html- prefix
    paper_id = id.replace("html-", "")

    response = requests.get(url)
    html_content = str(response.text)

    if ALLOW_DOWNLOAD: 
        if not os.path.exists(paths.HTML_FOLDER):
            os.makedirs(paths.HTML_FOLDER)
        
        with open(f"{paths.HTML_FOLDER}/{paper_id}.html", "w", encoding="utf-8") as file:
            file.write(html_content)

