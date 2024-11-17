import json
import os
from typing import List

import lxml.etree
import paths
from lxml import html
import lxml




# Function that filter table content
def table_filter(table_name, html_content):
    
        if html_content:
            
            to_embed: List[str] = []
            
            
            # HTML parsing with lxml
            tabTree = html.fromstring(html_content)

            # Find all <tr> tag from table (row)
            tr_elements = tabTree.xpath('//tr//text()')
            # print(tr_elements)
                
            for tr in tr_elements:
                tr_toString = str(tr)
                
                try:
                    
                    # Filter for numeric
                    float(tr_toString)
                    
                except ValueError:
                    
                    # Other filters
                    if not (tr_toString == "\n" or tr_toString == "(" or tr_toString == ")" 
                            or tr_toString == "⋅" or tr_toString == "=" or tr_toString == "." 
                            or tr_toString == ","or tr_toString == ":" or tr_toString == ";"
                            or tr_toString == "-" or tr_toString == "_"):
                        to_embed.append(tr_toString)
                    
            print(to_embed)
            return (" ".join(to_embed))


        else:
            print(f"Il file non contiene dati HTML validi nella tabella {table_name}.\n\n")
            return ""
        
    