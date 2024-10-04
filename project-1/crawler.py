import requests
from lxml import html

TOPIC = "cs.AI"
NUMBER_OF_PAPERS = 10

URL = f"https://arxiv.org/list/{TOPIC}/recent?skip=0&show={NUMBER_OF_PAPERS}"

response = requests.get(URL)

print("GET Response Status Code:", response.status_code)
if (response.status_code != 200):
    print("GET Request Failed")
    exit()

html_content = html.fromstring(response.content)

paper_urls = html_content.xpath('//*[@id="articles"]//dt//a[text()="html"]/@href')

for paper_url in paper_urls:
    
    response = requests.get(paper_url)
    html_content = html.fromstring(response.content)

    article = html_content.xpath('//article')[0]

    figures = article.xpath('//figure[contains(@class, "figure") and contains(@id, ".F")]')
    tables = article.xpath('//figure[contains(@class, "table") and contains(@id, ".T")]')

    for table in tables:
        caption = table.xpath('./figcaption/text()')
        print(caption)



