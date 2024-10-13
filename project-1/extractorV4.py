import json
import paths
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    paper_id: str = ""
    title: str = ""
    tables: list[TableData] = field(default_factory=list)


def extract_paper_title(paper: html.HtmlElement) -> str:
    title = paper.xpath('//title/text()')[0]
    return title


def extract_table_caption(table: html.HtmlElement, usedCaptions: set[str]) -> tuple[str, str]:
    
    # get the first valid caption found in the following xpaths
    xpaths = [
        './/preceding-sibling::*[contains(@class, "ltx_caption")][1]//text()',
        './/following-sibling::*[contains(@class, "ltx_caption")][1]//text()',
        './/preceding::*[contains(@class, "ltx_caption") and .//*[contains(@class, "ltx_tag_table")]][1]//text()',
        './/following::*[contains(@class, "ltx_caption") and .//*[contains(@class, "ltx_tag_table")]][1]//text()'
    ]

    for xpath in xpaths:
        caption_parts = table.xpath(xpath)
        
        if caption_parts:
            caption = ''.join(caption_parts)

            if caption not in usedCaptions:
                return caption, caption_parts[0]
    
    return '', ''


def extract_table(table: html.HtmlElement) -> str:
    return html.tostring(table).decode('utf-8')


def extract_table_footnotes(table: html.HtmlElement, table_id: str) -> list[str]:
    id = ".".join(table_id.split(".")[:2])
    table_container = table.xpath(f'.//ancestor::figure[@id="{id}"][0]')

    if not table_container:
        return []
    
    table_container = table_container[0]

    footnotes_xpath = table_container.xpath('.//*[contains(@id, "footnote") and not(contains(@id, "."))]')
    footnotes: list[str] = []
    
    for footnote in footnotes_xpath:
        footnote_segments = footnote.xpath('.//text()')
        
        if footnote_segments:
            foot_text = ""
            for segment in footnote_segments:
                if segment == "" or segment.isnumeric() or segment == "footnotetext: ":
                    continue
                foot_text += segment
            
            footnotes.append(foot_text)
    
    return footnotes


def extract_table_references(paper: html.HtmlElement, table_id: str, tableDenomination: str) -> list[str]:
    result = []

    # get the first two parts of the table id (e.g. #S1.T1.1.2 -> #S1.T1) because it's the id usally used in references
    id = ".".join(table_id.split(".")[:2])

    a_refs = paper.xpath(f'//a[contains(@href, "{id}")]/..')

    # first try to find references by looking for <a> tags
    if a_refs:
        for a_ref in a_refs:
            text_ref_content = a_ref.text_content().strip() if hasattr(a_ref, 'text_content') else a_ref.strip()
            result.append(text_ref_content)
    
    # if no references are found, try to find them by looking for text references
    elif tableDenomination != "":
        
        # find all text references that contain the table denomination followed by a space, a dot,
        # a colon or a comma. It's necessary to avoid selecting tables with a "greater" denomination.
        # (e.g. "Table 1" and "Table 11", or "Table II" and "Table III") 
        text_refs = paper.xpath(f'//*[contains(normalize-space(text()), "{tableDenomination} ") or '
                                f'contains(normalize-space(text()), "{tableDenomination}.") or '
                                f'contains(normalize-space(text()), "{tableDenomination}:") or '
                                f'contains(normalize-space(text()), "{tableDenomination},")]')

        for text_ref in text_refs: 
            text_ref_content = text_ref.text_content().strip() if hasattr(text_ref, 'text_content') else text_ref.strip()
    
            # if the text is exactly the table denomination followed by a colon, it's not a reference, but the caption
            if text_ref_content != tableDenomination + ":":
                result.append(text_ref_content)

    return result


def extract_paper_data(paper: html.HtmlElement, filename: str) -> PaperData:
    #TODO: check tables inside tables e.g. 2410.03131
    paperData = PaperData()

    tablesData: list[TableData] = []
    usedCaptions: set[str] = set()

    tables: list[html.HtmlElement] = paper.xpath('//table[contains(@class, "ltx_tabular")]')

    for table in tables:
        tableData = TableData()

        table_id = table.get('id')

        tableData.table_id = table_id
        
        tableData.caption, tableDenomination = extract_table_caption(table, usedCaptions)
        usedCaptions.add(tableData.caption)

        tableDenomination = tableDenomination.replace(":", "").strip()

        tableData.table = extract_table(table)
        tableData.footnotes = extract_table_footnotes(table, table_id)
        tableData.references = extract_table_references(paper, table_id, tableDenomination)

        tablesData.append(tableData)

    paperData.paper_id = filename
    paperData.title = extract_paper_title(paper)
    paperData.tables = tablesData

    return paperData
    

def process_file(filename, html_folder, json_folder):
    with open(f"{html_folder}/{filename}", "r", encoding="utf-8") as htmlFile:
        file_content = htmlFile.read().encode('utf-8')
        paper = html.fromstring(file_content, parser=html.HTMLParser())
        
        filename = filename.replace(".html", "")

        paperData = extract_paper_data(paper, filename)

        with open(f"{json_folder}/{filename}.json", "w", encoding="utf-8") as jsonFile:
            json.dump(paperData, jsonFile, default=lambda o: o.__dict__, indent=4)


if __name__ == "__main__":
    html_folder = paths.HTML_FOLDER
    json_folder = paths.JSON_FOLDER

    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    filenames = os.listdir(html_folder)

    max_workers = 8

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, filename, html_folder, json_folder): filename for filename in filenames}

        for future in tqdm(as_completed(futures), desc="Processing HTML files", unit=" file", colour="green", total=len(futures)):
            try:
                future.result() 
            except Exception as e:
                print(f"Error processing file {futures[future]}: {e}")



        