import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from tabulate import tabulate


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


def parse_html_table(html_table: str) -> str:
    """
    Function to parse an HTML table into a tabulated string representation.

    Args:
        html_table (str): The HTML table to parse.

    Returns:
        str: The tabulated DataFrame
    """
    html_buffer = StringIO(html_table)
    df = pd.read_html(html_buffer)[0].fillna('')
    
    return tabulate(df , headers="keys", tablefmt="pipe", showindex=False)


def parse_html_table_with_arbitrary_headers(html_table: str) -> str:
    """
    Parses an HTML table into a tabulated string, formatting arbitrarily nested headers into separate rows.

    Args:
        html_table (str): The HTML table to parse.

    Returns:
        str: The processed and tabulated string representation with nested headers formatted as separate rows.
    """
    html_buffer = StringIO(html_table)
    
    # Attempt to parse as a multi-level header table first
    try:
        df = pd.read_html(html_buffer, header=[0, 1, 2])[0].fillna('')
        is_multilevel = True
    except ValueError:
        try:
            # Try two-level headers
            df = pd.read_html(html_buffer, header=[0, 1])[0].fillna('')
            is_multilevel = True
        except ValueError:
            # Fallback to single header
            df = pd.read_html(html_buffer, header=0)[0].fillna('')
            is_multilevel = False

    if is_multilevel:
        # Combine multi-level headers into separate rows
        header_rows = []
        for level in range(df.columns.nlevels):
            header_rows.append([str(col) if col else '' for col in df.columns.get_level_values(level)])

        # Combine header rows with data rows
        data_rows = df.values.tolist()
        combined_rows = header_rows + data_rows

        # Tabulate the combined rows
        return tabulate(combined_rows, tablefmt="pretty")
    else:
        # Single header case: directly tabulate with headers
        return tabulate(df, headers="keys", tablefmt="pretty")