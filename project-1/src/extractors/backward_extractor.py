from json_schema import TableData
from lxml import html


def extract_table_caption(table: html.HtmlElement, usedCaptions: set[str]) -> tuple[str, str]:
    
    # get the first valid caption found in the following xpaths
    xpaths = [
        './/preceding-sibling::*[contains(@class, "ltx_caption")][1]//text()',
        './/following-sibling::*[contains(@class, "ltx_caption")][1]//text()',
        './/preceding::*[contains(@class, "ltx_caption") and .//*[contains(@class, "ltx_tag_table")]][1]//text()',
        './/following::*[contains(@class, "ltx_caption") and .//*[contains(@class, "ltx_tag_table")]][1]//text()',
        './/preceding::*[contains(@class, "ltx_caption")][1]//text()',
        './/following::*[contains(@class, "ltx_caption")][1]//text()'
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
    table_container = table.xpath(f'.//ancestor::figure[@id="{id}"][1]')

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
                                f'contains(normalize-space(text()), "{tableDenomination};") or '
                                f'contains(normalize-space(text()), "{tableDenomination},")]')

        for text_ref in text_refs: 
            text_ref_content = text_ref.text_content().strip() if hasattr(text_ref, 'text_content') else text_ref.strip()
    
            # if the text is exactly the table denomination followed by a colon, it's not a reference, but the caption
            if text_ref_content != tableDenomination + ":":
                result.append(text_ref_content)

    return result


def extract_paper_data(paper: html.HtmlElement) -> dict[str, TableData]:

    tablesData: dict[str, TableData] = {}
    usedCaptions: set[str] = set()

    tables: list[html.HtmlElement] = paper.xpath('//table[contains(@class, "ltx_tabular") and not(ancestor::table)]')

    for table in tables:
        tableData = TableData()

        table_id = table.get('id')
        
        tableData.caption, tableDenomination = extract_table_caption(table, usedCaptions)
        usedCaptions.add(tableData.caption)

        tableDenomination = tableDenomination.replace(":", "").strip()

        tableData.table = extract_table(table)
        tableData.footnotes = extract_table_footnotes(table, table_id)
        tableData.references = extract_table_references(paper, table_id, tableDenomination)

        tablesData[table_id] = tableData

    return tablesData
        