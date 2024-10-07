import requests
import paths
import os
from lxml import html

# Table
# Table caption
# Table footnotes
# Table references (paragraphs)

filenames = os.listdir(paths.HTML_FOLDER)

for file in filenames:
    with open(f"{paths.HTML_FOLDER}/{file}", "r", encoding="utf-8") as file:
        file_content = file.read()
        paper = html.fromstring(file_content)

        footnotes = paper.xpath('//figure[contains(@id, ".T")]//*[contains(@id, "footnote") and not(contains(@id, "."))]//text()')
        
        if footnotes != []: 
            for footnote in footnotes:
                if footnote == "" or footnote.isnumeric():
                    continue
                print(footnote)