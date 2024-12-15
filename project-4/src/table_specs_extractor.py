from table_processing import clean_table, parse_html_table
from llm import query_groq
from examples import example1
import paths
import json

def extract_table_specs(table_data: dict) -> str:
    """
    Function to extract specifications from a table in a research paper.

    Args:
        table_data (dict): The data of the table to extract specifications from.

    Returns:
        str: The extracted specifications from the table.
    """
    html_content = clean_table(table_data['table'])
    parsed_table = parse_html_table(html_content)

    system_prompt = f"""You are an expert in computer science and in understanding tables.
    Your task is to extract specifications from the table provided with its caption and references.

    Example: {example1}

    Response should only include the specifications from the table.
    Please provide the specifications from the following table:
    """

    content = f"""
    [Table]: 
    {parsed_table}
    [Caption]: 
    {table_data['caption']}
    [References]: 
    {table_data['references']}
    """
    return query_groq(messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": content
        }
    ])

if __name__ == "__main__":
    with open(paths.RAW + '/2303.00491.json', 'r') as file:
        data = json.load(file)
        table_data = data['S3.T1']

    response = extract_table_specs(table_data)

    print(response)

    