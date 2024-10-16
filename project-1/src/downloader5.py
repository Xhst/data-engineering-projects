import requests
import arxiv
import paths
import time
from lxml import html
import os

queries: dict[str, str] = {}
url_list: str = ""
file_count = 0

client = arxiv.Client()

queries['synthetic_data'] = '(ti:"synthetic data")'

if not os.path.exists(paths.HTML_FOLDER):
    os.makedirs(paths.HTML_FOLDER)

for topic, query in queries.items():
    
    if not os.path.exists(paths.HTML_FOLDER + "/" + topic):
        os.makedirs(paths.HTML_FOLDER + "/" + topic)

    search = arxiv.Search(
        query=query,
        max_results=700,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    for result in client.results(search):
        paper_id = result.get_short_id().split("v")[0]

        url = f"https://ar5iv.labs.arxiv.org/html/{paper_id}"

        time.sleep(0.5)

        response = requests.get(url, allow_redirects=False)

        if response.status_code in (301, 302, 307, 308):
            url = response.headers["Location"].replace("abs", "html")
            print(f"Redirected to {url}")
            response = requests.get(url, allow_redirects=False)

        if response.status_code == 404:
            print(f"404 Not Found for {url}")
            continue

        if response.status_code != 200:
            print(f"Failed to open {url}")
            continue

        if "reCAPTCHA" in response.text:
            print("reCAPTCHA detected")
            continue

        html_content = str(response.text)
        url_list += url + "\n"
        file_count += 1

        with open(f"{paths.HTML_FOLDER}/{topic}/{paper_id}.html", "w", encoding="utf-8") as file:
            file.write(html_content)    
    

with open(f"{paths.HTML_FOLDER}/urls.txt", "w", encoding="utf-8") as file:
    file.write(url_list)

print(f"Successfully downloaded {file_count} files.\n")