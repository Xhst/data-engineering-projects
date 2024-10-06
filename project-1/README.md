# Data Engineering - Project 1

### Assignment
- Choose a computer science research topic (e.g., query optimization) and download HTML scientific papers on the chosen topic 
- From the HTML source files, extract: 
    - tables 
    - tables’ captions 
    - footnotes in the tables or in the captions 
    - paragraphs containing references to the extracted tables
- For each paper:
    - Using XPATH, extract all the tables; 
    - for each table extract its caption, footnotes (if present), paragraphs with references to the table
    - Store the extracted data in a .json file, named exactly as the identifier 
- Structure of the json file:
```json
{ 
    "id_table_1": 
    {
        "caption": "text",
        "table": "html_table",
        "footnotes": ["footnote1", "footnote2", ...],
        "references": ["paragraph",  "paragraph", ...]
    },

    "id_table_2": {
        ...
    }, 
}

```
- Store the json files in a directory with name "extraction"
- To assess the quality of the extraction, check:
    - If all tables are extracted
    - If all footnotes and captions and paragraphs with references were extracted. If something is missing, refine the XPATH expression
    - Note that every table should have at least one referencing paragraph


