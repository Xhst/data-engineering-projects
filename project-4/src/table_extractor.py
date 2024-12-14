import pandas as pd
from bs4 import BeautifulSoup
import itertools
import json
import paths

def clean_table(html_table: str) -> str:
    """
    Function to clean an HTML table, removing all attributes and tags that are not part of the table structure.

    Args:
        html_table (str): The HTML table to clean.

    Returns:
        str: The cleaned HTML table.
    """
    soup = BeautifulSoup(html_table, "html.parser")

    # Tags that are part of the table structure and should be kept
    table_tags = ['table', 'tr', 'td', 'th', 'tbody', 'thead', 'tfoot']

    tags_to_remove = ['annotation', 'annotation-xml']

    for tag in soup.find_all(True):  
        # Remove id and class attributes
        if tag.attrs and 'id' in tag.attrs:
            del tag.attrs['id']
        if tag.attrs and 'class' in tag.attrs:
            del tag.attrs['class']

        # Remove tags that are not part of the table structure including their content
        if tag.name in tags_to_remove:
            tag.decompose()
            continue
        
        # Remove all tags that are not part of the table structure and keep their content
        if tag.name not in table_tags:
            try:
                tag.unwrap()
            except ValueError:
                tag.decompose()

    
    return soup.prettify()


def parse_html_table(html_table):
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_table, "html.parser")
    table = soup.find("table")

    if not table:
        raise ValueError("No table found in the provided HTML.")

    # Initialize grid for table data
    rows = table.find_all("tr")
    max_cols = max(
        sum(int(cell.get("colspan", 1)) for cell in row.find_all(["td", "th"]))
        for row in rows
    )
    grid = [[None] * max_cols for _ in range(len(rows))]

    for row_idx, row in enumerate(rows):
        col_idx = 0
        for cell in row.find_all(["td", "th"]):
            # Skip filled cells
            while col_idx < max_cols and grid[row_idx][col_idx] is not None:
                col_idx += 1

            # Extract cell attributes
            content = cell.get_text(strip=True)
            rowspan = int(cell.get("rowspan", 1))
            colspan = int(cell.get("colspan", 1))

            # Fill grid positions
            for i, j in itertools.product(
                range(row_idx, row_idx + rowspan),
                range(col_idx, col_idx + colspan),
            ):
                grid[i][j] = content

            col_idx += colspan

    # Process headers and data
    headers = grid[0]
    data = [dict(zip(headers, row)) for row in grid[1:] if any(row)]

    return data


if __name__ == "__main__":
    with open(paths.RAW + '/2409.17364.json', 'r') as file:
        data = json.load(file)
        html_content = data['S4.T3']['table']
    
    html_content = clean_table(html_content)

    print(html_content)
    
    #parsed_table = parse_html_table(html_content)
    #print(json.dumps(parsed_table, indent=4))