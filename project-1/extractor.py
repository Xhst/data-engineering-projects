import json
from json_schema import TableSchema
import typing
import paths
import os
from lxml import html

# for every article
    # initialize json
    # extract TableSchemas
    # for every table
        # TableSchema caption
        # TableSchema footnotes
        # TableSchema references (paragraphs)
        # add to json
    # save json with article id

filenames = os.listdir(paths.HTML_FOLDER)

for file in filenames:
    article_json : dict[str, TableSchema] = {}
    
    with open(f"{paths.HTML_FOLDER}/{file}", "r", encoding="utf-8") as file:
        file_content = file.read()
        paper = html.fromstring(file_content)

        # Extracting tables
        tables = paper.xpath('//figure[contains(@id, ".T")]')
        
        for table in tables:
            table_json : TableSchema = {}
            # we extract the table id and format it like this: T1, T2, T3, ...
            table_id = table.xpath('@id')[0].split(".")[1]
            
            # Extracting captions
            caption = table.xpath('//figcaption//text()')
        
            # Extracting footnotes
            footnote_segments = table.xpath('//*[contains(@id, "footnote") and not(contains(@id, "."))]//text()')
            
            if footnote_segments != []:
                foot_text = ""
                for segment in footnote_segments:
                    if segment == "" or segment.isnumeric():
                        continue
                    foot_text += segment
                    
                print(foot_text)
            
            # Extracting references
            
            # This extracts all the references of the table, and then search for the first ancestor section of the reference,
            # then takes its child which contains the section title
            paragraphs_ref = paper.xpath('//a[contains(@href, "{table_id}") and contains(@class, "ltx_ref")]/ancestor::section[1]/*[contains(@class, "ltx_title")]')
            
            ref_titles : list[str] = []
            for par in paragraphs_ref:
                sec_title = ""
                title_fragments = par.xpath('.//text()')
                for fragment in title_fragments:
                    if fragment == "" or fragment == "\n":
                        continue
                    sec_title += fragment
                
                ref_titles.append(sec_title)
                
            # to continue
            
        # save json
        json.dump