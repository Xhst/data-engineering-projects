from lxml import html
from json_schema import TableData


def extract_references(table_num: str, table_id : str, paper : html.HtmlElement) -> list[str]:
    """
    Extracts paragraphs text where references to the table are found.

    It searches for all the references linked to a specific table ID, then finds the paragraph containing the reference.

    Parameters:
        table_id (str): The table ID we are searching the references for.
        paper (html.HtmlElement): The paper HTML element from which to extract the references and section titles.

    Returns:
        list[str]: A list of section titles associated with the references to the table.
    """
    refs_text: list[str] = []
    
    paragraphs_ref = paper.xpath(f'//a[contains(@href, {table_id})]/..')
    
    # If there are no link references, we try to find the ref by table number text (es. "Table 1")
    if paragraphs_ref == []:
        paragraphs_ref = paper.xpath(f'//p[contains(normalize-space(text()), "{table_num} ") or '
                                         f'contains(normalize-space(text()), "{table_num}.") or '
                                         f'contains(normalize-space(text()), "{table_num};") or '
                                         f'contains(normalize-space(text()), "{table_num},")]')
    
    for par in paragraphs_ref:
        par_text = ""
        segments = par.xpath('.//text()')
        for seg in segments:
            par_text = par_text + seg
        refs_text.append(par_text)
    
    return refs_text


def extract_caption(table: html.HtmlElement, table_id: str) -> str:
    # Extracting captions ("Table X: " + "caption")
    caption_fragments = table.xpath('.//*[contains(@class, "ltx_caption")]//text()')
    # If we did not found any caption, we try a stricter rules
    if caption_fragments == []:
        caption_fragments = table.xpath(f'./p[contains(@id, "{table_id}.")]//text()')
    if caption_fragments == []:
        caption_fragments = table.xpath(f'./span[contains(@id, "{table_id}.")]//text()')

    caption = "".join(caption_fragments)
    
    return caption

        
def extract_footnotes(table : html.HtmlElement) -> list[str]:
    """
    Extracts the footnotes from the table by combining the non-numeric text segments 
    of each footnote, ignoring specific nested elements.
    
    The structure of every footnote seems to be:
        footnote id = "footnote1" (the most outer part)\n
        |__> footnote id = "footnote1.1" (an hidden html element that appears 
                when mouse hovering -> which we are not interested in)\n
            |__> several text fragments componing the footnote (we take these directly from the first element)

    Of these fragments, the first ones are usually the footnote number repeated, so we can ignore them
    Then, we combine the rest
    
    Parameters:
        table (html.HtmlElement): The table element from which to extract the footnotes.

    Returns:
        list[str]: A list of strings where each string is a table footnote's full text.
    """
    footnotes_xpath = table.xpath('.//*[contains(@id, "footnote") and not(contains(@id, "."))]')
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

        
def extract_paper_data(paper: html.HtmlElement) -> dict[str, TableData]:
    article_json : dict[str, TableData] = {}
                    
    # Extracting tables, here "tables" are intended as tags containing table tags

    # Most tables are contained within a figure element with a class of "ltx_table" and id containing ".T", 
    # while in rare cases they are contained within a div element with a class of "ltx_minipage".
    # In that case, we select only those divs that contain a table element.
    table_containers = paper.xpath('//figure[contains(@id, ".T") and contains(@class, "ltx_table")] | ' + 
                                   '//table/ancestor::div[contains(@id, ".") and contains(@class, "ltx_minipage")]')

    for table in table_containers:
        if table == None or table == [] or not(table.getchildren()):
            continue
        
        # we exclude equations and figures (id = ".E" or ".F")
        table_tags = table.xpath('.//table[contains(@id, ".T")]')
    
        table_id = table.get('id')
        
        # Extracting caption
        caption = extract_caption(table, table_id)

        # Extracting footnotes
        footnotes = extract_footnotes(table)
        
        # Extracting references
        # We need this to search for some references, we take the first part of the caption ("Table X:")
        table_num = caption.split(":")[0]
        paragraphs_refs = extract_references(table_num, table_id, paper)

        
        # If there are no tables, we may have found a table caption related to a <table> tag
        # that is not a direct parent of the table element, or maybe is outside of the figure element. 
        # In this case, we need to add the caption to the
        # exisitng table JSON and add footnotes that may lay inside the caption
        if table_tags == []:
            if table_id in article_json:
                article_json[table_id].caption = caption
                existing_footnotes: set[str] = set(article_json[table_id].footnotes)
                existing_footnotes.update(footnotes)
                article_json[table_id].footnotes = list(existing_footnotes)
        
        else:
            # If there are tables, we just insert it into the JSON
            table_tag_str = ""
            for table_tag in table_tags:
                table_tag_str = table_tag_str + html.tostring(table_tag).decode('utf-8')

            # populate TableData
            table_json = TableData()
            table_json.caption = caption
            table_json.table = table_tag_str
            table_json.footnotes = footnotes
            table_json.references = paragraphs_refs
            
            # Store the table JSON with its id
            article_json[table_id] = table_json
        
    return article_json
