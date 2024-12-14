import pandas as pd
from bs4 import BeautifulSoup
import os
from groq import Groq
import json
import paths
from dotenv import load_dotenv
from pathlib import Path
from io import StringIO
from tabulate import tabulate

load_dotenv(dotenv_path=Path('../.env'))

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


def parse_html_table(html_table: str):
    html_buffer = StringIO(html_table)
    df = pd.read_html(html_buffer)[0]
    df_list = df.values.tolist()

    return tabulate(df_list[1:], headers='keys', tablefmt='pipe')


if __name__ == "__main__":
    with open(paths.RAW + '/2409.17364.json', 'r') as file:
        data = json.load(file)
        html_content = data['S4.T3']['table']
    
    html_content = clean_table(html_content)
    
    parsed_table = parse_html_table(html_content)

    print(parsed_table)

    content = """
    {table} 

    Extract data from this table.
    """.format(table=parsed_table)

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    print(chat_completion.choices[0].message.content)