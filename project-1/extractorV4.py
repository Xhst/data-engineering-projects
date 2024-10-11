import json
import paths
import os
from dataclasses import dataclass, field
from tqdm import tqdm
from lxml import html

@dataclass
class TableData:
    table_id: str = ""
    caption: str = ""
    table: str = ""
    footnotes: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)

@dataclass
class PaperData:
    filename: str = ""
    title: str = ""
    tables: list[TableData] = field(default_factory=list)

def extract_paper_title(paper: html.HtmlElement) -> str:
    title = paper.xpath('//title/text()')[0]
    return title

def extract_table_caption(table: html.HtmlElement) -> tuple[str, str]:

    # try find caption from preceding sibling
    caption_parts = table.xpath('.//preceding-sibling::*[contains(@class, "ltx_caption")]//text()')

    if caption_parts:
        return "".join(caption_parts), caption_parts[0]
    
    # try find caption from following sibling
    caption_parts = table.xpath('.//following-sibling::*[contains(@class, "ltx_caption")]//text()')

    if caption_parts:
        return "".join(caption_parts), caption_parts[0]
    
    # try find caption from parent
    caption_parts = table.xpath('.//parent::*[contains(@class, "ltx_caption")]//text()')

    if caption_parts:
        return "".join(caption_parts), caption_parts[0]
    
    return "", ""


def extract_table(table: html.HtmlElement) -> str:
    return html.tostring(table).decode('utf-8')

def extract_table_footnotes(table: html.HtmlElement) -> list[str]:
    return []

def extract_table_references(paper: html.HtmlElement, table_id: str, tableDenomination: str) -> list[str]:
    result = []

    # get the first two parts of the table id (e.g. #S1.T1.1.2 -> #S1.T1) because it's the id usally used in references
    table_id = ".".join(table_id.split(".")[:2])

    a_refs = paper.xpath(f'//a[contains(@href, "{table_id}")]')

    # first try to find references by looking for <a> tags
    if a_refs:
        for a_ref in a_refs:
            ref = a_ref.xpath('ancestor::section')
            if ref:
                result.append(html.tostring(ref[0]).decode('utf-8'))
    
    # if no references are found, try to find them by looking for text references
    else:
        text_refs = paper.xpath(f'//*[contains(text(), "{tableDenomination}") and not(contains(@class, "ltx_text"))]')

        for text_ref in text_refs:
            ref = text_ref.xpath('ancestor::section')
            if ref:
                result.append(html.tostring(ref[0]).decode('utf-8'))

    return result


def extract_paper_data(paper: html.HtmlElement, filename: str) -> PaperData:
    paperData = PaperData()

    tablesData: list[TableData] = []

    tables: list[html.HtmlElement] = paper.xpath('//table[contains(@id, ".T") or contains(@id, ".F")]')

    for table in tables:
        tableData = TableData()

        table_id = table.get('id')

        tableData.table_id = table_id
        tableData.caption, tableDenomination = extract_table_caption(table)

        tableDenomination = tableDenomination.replace(":", "").strip()

        tableData.table = extract_table(table)
        tableData.footnotes = extract_table_footnotes(table)
        tableData.references = extract_table_references(paper, table_id, tableDenomination)

        tablesData.append(tableData)

    paperData.filename = filename
    paperData.title = extract_paper_title(paper)
    paperData.tables = tablesData

    with open(f"{paths.JSON_FOLDER}/{filename}.json", "w", encoding="utf-8") as file:
        json.dump(paperData, file, default=lambda o: o.__dict__, indent=4)
    


if __name__ == "__main__":
    filenames = os.listdir(paths.HTML_FOLDER)

    # make sure the JSON folder exists
    if not os.path.exists(paths.JSON_FOLDER):
        os.makedirs(paths.JSON_FOLDER)

    for filename in tqdm(filenames, desc="Processing HTML files", unit=" file", colour="green", disable=False):
        with open(f"{paths.HTML_FOLDER}/{filename}", "r", encoding="utf-8") as file:
            file_content = file.read().encode('utf-8')
            paper = html.fromstring(file_content, parser=html.HTMLParser())
            
            filename = filename.replace(".html", "")

            extract_paper_data(paper, filename)



        