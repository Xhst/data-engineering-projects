import json
import paths
import os
from tqdm import tqdm
from lxml import html

# Set this to True if you want to check if the HTML files contain tables
CHECK_TABLE_PRESENCE = False

def extract_references(table_number : str, paper : html.HtmlElement) -> list[str]:
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
    # this almost works, but it could finds also tables with number table_number0,1,2,3, ex we search for 1 and find also 10
    paragraphs_ref = paper.xpath(f'//p[contains(text(),"{table_number} ") or contains(text(),"{table_number}.") or contains(text(),"{table_number},") or contains(text(),"{table_number}-")]')
    
    refs_text: list[str] = []
    
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


papers_no_tables: list[str] = []

if __name__ == "__main__":
    filenames = os.listdir(paths.HTML_FOLDER)

    # make sure the JSON folder exists
    if not os.path.exists(paths.JSON_FOLDER):
        os.makedirs(paths.JSON_FOLDER)

    for filename in tqdm(filenames, desc="Processing HTML files", unit=" file", colour="green", disable=False):
        article_json : dict[str, dict] = {}
        
        with open(f"{paths.HTML_FOLDER}/{filename}", "r", encoding="utf-8") as file:
            file_content = file.read()
            paper = html.fromstring(file_content)

            if CHECK_TABLE_PRESENCE:
                all_table_tags: list[html.HtmlElement] = paper.xpath('//table[not(contains(@id, ".E") or contains(@id, ".F"))]')
                if all_table_tags == []:
                    papers_no_tables.append(filename.replace(".html", ""))
                        
            # Extracting tables, here "tables" are intended as tags containing table tags
            
            # Most tables are contained within a figure element with a class of "ltx_table" and id containing ".T", 
            # while in rare cases they are contained within a div element with a class of "ltx_minipage".
            # In that case, we select only those divs that contain a table element.
            tables = paper.xpath('//figure[contains(@id, ".T") and contains(@class, "ltx_table")] | ' + 
                                 '//table/ancestor::div[contains(@id, ".") and contains(@class, "ltx_minipage")]')
        
            for table in tables:
                if table == None or table == [] or not(table.getchildren()):
                    continue
                
                table_tags = table.xpath('.//table[contains(@id, ".T")]')
            
                # we extract the table id and format it like this: T1, T2, T3, ...
                table_id = ".".join(table.xpath('@id')[0].split(".")[1:])
                
                # Extracting caption
                caption = extract_caption(table, table_id)

                # Extracting footnotes
                footnotes = extract_footnotes(table)
                
                # Extracting references
                # We need this to search for references, we take the first part of the caption ("Table X:")
                table_number = caption.split(":")[0]
                paragraphs_refs = extract_references(table_number, paper)
                
                # Finally, some ids are missing the "T" prefix, so we add it
                if not("T" in table_id):
                    table_id = "T" + table_id

                table_str = ""
                # If there are tables, we insert it into the JSON
                if table_tags != []:
                    for table_tag in table_tags:
                        table_str = table_str + html.tostring(table_tag).decode('utf-8')

                    table_json = {
                        "caption": caption,
                        "table": table_str,
                        "footnotes": footnotes,
                        "references": paragraphs_refs
                    }
                    
                    # Store the table JSON with its id
                    article_json[table_id] = table_json
                
                else:
                    # If there are no tables, we may have found a table caption related to a <table> tag
                    # that is not a direct parent of the table element, or maybe is outside of the figure element. 
                    # In this case, we need to add the caption to the
                    # exisitng table JSON and add footnotes that may lay inside the caption
                    if table_id in article_json:
                        article_json[table_id]["caption"] = caption
                        existing_footnotes: set[str] = set(article_json[table_id]["footnotes"])
                        existing_footnotes.update(footnotes)
                        article_json[table_id]["footnotes"] = list(existing_footnotes)
                
        # Change extension to json and save to file
        filename = filename.replace(".html", ".json")
        with open(f"{paths.JSON_FOLDER}/{filename}", "w", encoding="utf-8") as json_file:
            json.dump(article_json, json_file, indent=4)
