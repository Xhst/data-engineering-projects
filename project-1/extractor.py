import json
from json_schema import TableSchema
import paths
import os
from lxml import html


def extract_references(table_id : str, paper : html.HtmlElement) -> list[str]:
    """
    Extracts section titles where references to the table are found.

    It searches for all the references linked to a specific table ID, then finds the first ancestor
    section of that reference, and extracts the section title fragments contained within that section.

    Parameters:
        table_id (str): The table ID we are searching the references for.
        paper (html.HtmlElement): The paper HTML element from which to extract the references and section titles.

    Returns:
        list[str]: A list of section titles associated with the references to the table.
    """
    paragraphs_ref = paper.xpath('//a[contains(@href, "{table_id}") and contains(@class, "ltx_ref")]/ancestor::section[1]/*[contains(@class, "ltx_title")]')
    
    ref_titles: list[str] = []
    for par in paragraphs_ref:
        # Build each section title from the fragments
        sec_title = ""
        title_fragments = par.xpath('.//text()')
        for fragment in title_fragments:
            if fragment == "" or fragment == "\n":
                continue
            sec_title += fragment
        
        ref_titles.append(sec_title)
    
    return ref_titles

        
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
    footnotes_xpath = table.xpath('//*[contains(@id, "footnote") and not(contains(@id, "."))]')
    footnotes: list[str] = []
    
    for footnote in footnotes_xpath:
        footnote_segments = footnote.xpath('.//text()')
        
        if footnote_segments:
            foot_text = ""
            for segment in footnote_segments:
                if segment == "" or segment.isnumeric():
                    continue
                foot_text += segment
            
            footnotes.append(foot_text)   
            print(foot_text)
    
    return footnotes


if __name__ == "__main__":
    filenames = os.listdir(paths.HTML_FOLDER)

    # make sure the JSON folder exists
    if not os.path.exists(paths.JSON_FOLDER):
        os.makedirs(paths.JSON_FOLDER)

    for filename in filenames:
        article_json : dict[str, TableSchema] = {}
        
        with open(f"{paths.HTML_FOLDER}/{filename}", "r", encoding="utf-8") as file:
            file_content = file.read()
            paper = html.fromstring(file_content)

            # Extracting tables
            tables = paper.xpath('//figure[contains(@id, ".T")]')
            
            for table in tables:
                table_json : TableSchema = {}
                
                # we extract the table id and format it like this: T1, T2, T3, ...
                table_id = table.xpath('@id')[0].split(".")[1]
                
                # Extracting captions ("Table X: " + "caption")
                caption_fragments = table.xpath('//figcaption//text()')
                caption = "".join(caption_fragments)
            
                # Extracting footnotes
                footnotes = extract_footnotes(table)
                
                # Extracting references
                paragraphs_refs = extract_references(table_id, paper)
                
                table_json: TableSchema = {
                    "caption": caption,
                    "table": html.tostring(table).decode('utf-8'),  # Convert the table HTML element to string
                    "footnotes": footnotes,
                    "references": paragraphs_refs
                }
                
                # Store the table JSON with its id
                article_json[table_id] = table_json
            
            # Change extension to json and save to file
            filename = filename.replace(".html", ".json")
            with open(f"{paths.JSON_FOLDER}/{filename}", "w", encoding="utf-8") as json_file:
                json.dump(article_json, json_file, indent=4)
