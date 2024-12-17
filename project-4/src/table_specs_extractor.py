from table_processing import clean_table, parse_html_table
from llm import query_groq
from examples import example1, example2, example3
import paths
import json

def extract_table_claims(table_data: dict) -> str:
    """
    Function to extract claims from a table in a research paper.

    Args:
        table_data (dict): The data of the table to extract claims from.

    Returns:
        str: The extracted claims from the table.
    """
    html_content = clean_table(table_data['table'])
    parsed_table = parse_html_table(html_content)
    
    print(parsed_table)

    system_prompt = """You are an expert in computer science and in understanding tables.
    Your task is to extract claims from the table provided with its caption and references in this format:
    |{|Specification 1, Value|, |Specification 2, Value|}, Metric, Metric Value|

    Example: """ + example3.__str__() + """
    ---
    """

    content = f"""
    Please provide the claims from the following table:
    [Table]: 
    {parsed_table}
    [Caption]: 
    {table_data['caption']}
    [References]: 
    {table_data['references']}
    
    ---
    
    Response must only include the claims from the table.
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
    with open(paths.RAW + '/2206.10526.json', 'r') as file:
        data = json.load(file)
        table_data = data['S3.T1']

    response = extract_table_claims(table_data)

    print("\n\033[92mLLM response:\033[0m\n")
    print(response)

    