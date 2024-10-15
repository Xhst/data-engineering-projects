import json
import paths
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from lxml import html
from extractors import forward_extractor, backward_extractor, simple_forward_extractor


def process_file(filename: str, source_folder: str, extract_folder: str):
    with open(f"{source_folder}/{filename}", "r", encoding="utf-8") as htmlFile:
        file_content = htmlFile.read().encode('utf-8')
        paper = html.fromstring(file_content, parser=html.HTMLParser())
        
        filename = filename.replace(".html", "")
        
        # we extract the tables and sort them by id
        paperData = dict(sorted(forward_extractor.extract_paper_data(paper).items()))

        with open(f"{extract_folder}/{filename}.json", "w", encoding="utf-8") as jsonFile:
            json.dump(paperData, jsonFile, default=lambda o: o.__dict__, indent=4)


if __name__ == "__main__":
    html_folder = paths.HTML_FOLDER
    json_folder = paths.JSON_FOLDER

    folders_to_extract = ['record_linkage', 'synthetic_data']

    for folder in folders_to_extract:
        if not os.path.exists(f"{json_folder}/{folder}"):
            os.makedirs(f"{json_folder}/{folder}")

    filenames = os.listdir(html_folder)

    max_workers = 8
 
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for folder in folders_to_extract:

            extract_folder = f"{json_folder}/{folder}"
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
