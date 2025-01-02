from table_processing import clean_table, parse_html_table
from llm import query_groq
from examples import example1, example2_short, example_metric_column, example_data_table
import claim_builder
import paths
import json
import os
import time

def save_llm_response(response, paperId, tableId):
    """
    Saves the LLM response content to a file.

    Args:
        response (str): The response content to save.
        paperId (str): The paper ID.
        tableId (str): The table ID.
    """

    filename = f"{paperId}_{tableId}_llmResponse.txt"
    
    try:
        with open(paths.LLM_RESPONSE + "/" + filename, 'w', encoding='utf-8') as file:
            file.write(response)
        print(f"Response successfully saved to: {filename}")
    except Exception as e:
        print("\033[91m" + f"Error while saving the file: {e}" + "\033[0m")


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
    
    #print(parsed_table)

    system_prompt = """(forget the previous answers) You are an expert in computer science and in understanding tables.
    Your task is to extract claims from papers' tables provided with their captions and references in this format:
    |{|Specification 1, Value|, |Specification 2, Value|}, Metric, Metric Value|
    
    Remember that most of the times the caption and references retian most of the semantic information to infer the metrics or the specifications.
    When no metrics are inside the table (data table) we only want the specifications included, without any "metric" field (after each claim, move to a new line).
    ---
    Example 1 with metrics: """ + example1.__str__() + """
    ---
    Example 2 with metrics: """ + example2_short.__str__() + """
    ---
    Example 3 with metrics: """ + example_metric_column.__str__() + """
    ---
    Example without metrics: """ + example_data_table.__str__() + """
    ---
    If you find the dataset mentioned in the text, include it as a specification.
    ---
    Response MUST only include the claims, nothing else.
    """
    
    content = f"""
    Please provide the claims from the following table:
    [Table]: 
    {parsed_table}
    [Caption]: 
    {table_data['caption']}
    [References]: 
    {table_data['references']}
    
    """ # TODO: questo pezzo può essere tolto, per ora non si comporta benissimo POTREBBE ESSE UNA BUONA IDEA
    #These are some claims from the same paper for context:
    #""" + """|{|Dataset, ID|, |Range, [1,60]|, |Number of Integers, 5|, |Fine-tuned on, 1M|}, Zero-shot pass@1, 0.224|
    #|{|Dataset, Numerical OOD|, |Range, [1,100]|, |Number of Integers, 7|, |Fine-tuned on, 100M|}, Zero-shot pass@1, 0.315|
    #|{|Dataset, Form OOD|, |Range, [1,60]|, |Number of Integers, 8|, |Fine-tuned on, 1M|}, Zero-shot pass@1, 0.169|
    """---
    Response MUST only include the claims, nothing else.
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

    if not os.path.exists(paths.CLAIMS):
        os.makedirs(paths.CLAIMS)
        print(f"\033[32mCreated directory: {paths.CLAIMS}\033[0m\n")

    if not os.path.exists(paths.LLM_RESPONSE):
        os.makedirs(paths.LLM_RESPONSE)
        print(f"\033[32mCreated directory: {paths.LLM_RESPONSE}\033[0m\n")

    start_time = time.time()
    
    gt_path_papers = paths.GROUND_TRUTH.PAPERS
    
    for filename in os.listdir(gt_path_papers):
        if filename.endswith('.json'):
            file_path = os.path.join(gt_path_papers, filename)

            print(f"\n\033[94mProcessing file: {filename.rstrip('.json')}\033[0m")

            with open(file_path, 'r') as file:
                data = json.load(file)

            start_nested_time = time.time()

            for table_key, table_data in data.items():
        
                response = extract_table_claims(table_data)
                save_llm_response(response, filename.rstrip('.json'), table_key)

                print("\033[96mCreating claims file for table " + table_key + "\033[0m")
                claim_builder.build(response, filename.rstrip('.json'), table_key, paths.CLAIMS)
            end_nested_time = time.time()
            elapsed_nested_time = end_nested_time - start_nested_time
            print(f"\n\033[96m{filename.rstrip('.json')} completed successfully\033[0m ({elapsed_nested_time:.2f}s)")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nPapers claims built in {elapsed_time:.2f}s.")

    
'''
# DA RIVEDERE S4.T4 DI 1812.05040 (del GT)

if __name__ == "__main__":
    with open(paths.RAW + '/1911.07164.json', 'r') as file:
        data = json.load(file)
        table_data = data['S5.T2']

    response = extract_table_claims(table_data)

    print("\n\033[92mCreating claims files...\033[0m\n")
    print(response)
    claim_builder.build(response, "prova", "prv")
'''
    