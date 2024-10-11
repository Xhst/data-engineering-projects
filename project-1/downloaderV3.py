import requests
import arxiv
import paths
import time
from lxml import html

# Definisci la query
query = '(abs:"record linkage" OR abs:"entity resolution")'

# Ricerca su arXiv con limite di 5 articoli per esempio
search = arxiv.Search(
    query=query,
    max_results=1000,
    sort_by=arxiv.SortCriterion.SubmittedDate,
)

print(f"Query: {query}")

for result in search.results():
    paper_id = result.get_short_id().split("v")[0]

    ar5iv_url = f"https://ar5iv.labs.arxiv.org/html/{paper_id}"

    time.sleep(0.5)

    response = requests.get(ar5iv_url)

    if response.status_code != 200:
        print(f"Failed to open {ar5iv_url}")
        continue

    if "reCAPTCHA" in response.text:
        print("reCAPTCHA detected")
        continue

    html_content = str(response.text)

    with open(f"{paths.HTML_FOLDER}/{paper_id}.html", "w", encoding="utf-8") as file:
            file.write(html_content)    