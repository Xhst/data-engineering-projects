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

### Edge cases
#### Captions
Our xpath to retrieve tables was `//figure[contains(@id, ".T")`, which we used concatenated with other xpath to retrieve information in the inner html of the table such as caption, also retrieved empty tables that are not shown on the screen.
We updated the xpath to `//figure[contains(@id, ".T") and @class="ltx_table"]` and fixed the issue: the missing captions dropped from $12$ to $8$.

With the xpath we firstly used to retrieve captions (`.//figcaption//text()`) we had $8$ tables with no retrieved caption still.
We analyzed the source code of one of those paper (2410.02744) and, in fact the caption is inside a `span` tag.
We changed our xpath to `.//*[contains(@class, "ltx_caption")]//text()`, because all the papers using `figcaption` tag also has
`ltx_caption` class, we now had $7$ tables with missing caption.

The remaining 7 missing captions are from tables:
- Table 6 from 2410.01064
- Table 2 from 2410.01444
- Table 1, 5 and 8 from 2410.01927
- Table 6 from 2410.04795
We manually checked those tables and they actually have no caption.

#### Tables
We are still missing tables in 79 papers because they are not inside figure tags, or the id format is not consistent. 

Tables can be inside divs with strange structure, but this is a rare case (see paper 2406.19271)

The other major differences were that the table tag was used in some papers (∿40) to display equations (not an error then, no tables are really present)

Another problem was that the xpath `//figure[contains(@id, ".T") and @class="ltx_table"]` was excluding tables with other appended classes.

In some other cases (3 cases), table tags were used to display figures (see 2410.00031)

Then the last 3 cases left were checked manually:
- In paper 2410.03747 table tags were used to give structure to some authors bibliography
- In paper 2410.01821 table tags were used to display an equation inside a blockquote element
- In paper 2410.04245 there was a table tag with id="Thmexample2.p2.8" used to display function values examples


