from lxml import html

def table_filter(html_content: str) -> str:            
    to_embed: list[str] = []

    tabTree = html.fromstring(html_content)

    # Find all <tr> tag from table (row)
    tr_elements = tabTree.xpath('//tr//text()')
        
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
                    or tr_toString == "-" or tr_toString == "_" or tr_toString == "["
                    or tr_toString == "]" or tr_toString == "{" or tr_toString == "}"):
                to_embed.append(tr_toString)

    return (" ".join(to_embed))