import json
import paths
import os

from dataclasses import dataclass, field
from lxml import html

@dataclass
class TableData:
    table_id: str = "" 
    caption: str = ""
    footnotes: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)


def get_table_from_figure(figure):

    #return table 
     return


def get_caption_from_figure(figure):
     
     #return caption
     return

def get_footnotes_from_figure(figure):
     
     #return footnotes
     return

def get_references_from_figure(figure):
     
     #return references
     return




# simple extraction from figures
if __name__ == "__main__":
    filenames = os.listdir(paths.HTML_FOLDER)
        
    # make sure the JSON folder exists
    if not os.path.exists(paths.JSON_FOLDER):
            os.makedirs(paths.JSON_FOLDER)

    for filename in filenames:
        with open(f"{paths.HTML_FOLDER}/{filename}", "r", encoding="utf-8") as file:
            file_content = file.read().encode('utf-8')
            paper = html.fromstring(file_content, parser=html.HTMLParser())
            filename = filename.replace(".html", "")
                 
            table_data_list: list[TableData] = []
            figure_list: list[html.HtmlElement] = paper.xpath('//figure[contains(@id, ".T")]')

            for figure in figure_list:
                figure_data = TableData()
                figure_id = figure.get('id')
                
                table = get_table_from_figure(figure)
                caption = get_caption_from_figure(figure)
                footnotes = get_footnotes_from_figure(figure)
                references = get_references_from_figure(figure)
