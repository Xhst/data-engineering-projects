from lxml import html
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import json
import sys
import os

# Add the path of the external module to sys.path
sys.path.append(os.path.abspath('../'))

# Now you can import the module
import paths

def extract_paper_data(paper: html.HtmlElement) -> list[str]:
    tableIds : list[str] = []

    tables: list[html.HtmlElement] = paper.xpath('//table')    
    
    for table in tables:
        table_id = "no_id"

        if table.get('id'):
            table_id = table.get('id')
        
        # Store the table JSON with its id
        tableIds.append(table_id)
    
    return tableIds


def process_file(filename: str, source_folder: str, extract_folder: str):
    with open(f"{source_folder}/{filename}", "r", encoding="utf-8") as htmlFile:
        file_content = htmlFile.read().encode('utf-8')
        paper = html.fromstring(file_content, parser=html.HTMLParser())
        
        filename = filename.replace(".html", "")
        
        # we extract the tables and sort them by id
        paperData = sorted(extract_paper_data(paper))

        with open(f"{extract_folder}/{filename}.json", "w", encoding="utf-8") as jsonFile:
            json.dump(paperData, jsonFile, indent=4)


if __name__ == "__main__":
    html_folder = "../" + paths.HTML_FOLDER
    json_folder = "../" + paths.JSON_FOLDER

    folders_to_extract = ['synthetic_data']

    for folder in folders_to_extract:
        if not os.path.exists(f"{json_folder}/all_tags"):
            os.makedirs(f"{json_folder}/all_tags")

    filenames = os.listdir(html_folder)

    max_workers = 8
 
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for folder in folders_to_extract:

            extract_folder = f"{json_folder}/all_tags"
            source_folder = f"{html_folder}/{folder}"

            filenames = os.listdir(f"{source_folder}")

            futures = {
                executor.submit(process_file, filename, source_folder, extract_folder): filename for filename in filenames
            }

            for future in tqdm(as_completed(futures), desc=f"Processing {source_folder}", unit=" file", colour="green", total=len(futures)):
                try:
                    future.result() 
                except Exception as e:
                    print(f"Error processing file {futures[future]}: {e}")
