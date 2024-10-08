import json
import os
import paths
from tqdm import tqdm
from json_schema import TableSchema


filenames = os.listdir(paths.JSON_FOLDER)

total_files = len(filenames)

num_table_dict = {}
num_footnotes_dict = {}

num_articles_extra_ref = 0

total_tables = 0
total_footnotes = 0
total_references = 0


for filename in tqdm(filenames, desc="Processing JSON files", unit=" file", colour="green", disable=True):

    num_tables = 0
    num_footnotes = 0
    num_references = 0

    with open(f"{paths.JSON_FOLDER}/{filename}", "r", encoding="utf-8") as file:
        data = json.load(file)
        
        for table_id in data:
            table = data[table_id]
 
            footnotes = table['footnotes']
            references = table['references']

            if table['table']:
                num_tables += 1

            if footnotes:
                num_footnotes += len(footnotes)
            
            if references:
                num_references += len(references)

    if num_tables < num_references:
        num_articles_extra_ref += 1

    if num_footnotes > 500:
        print(filename)

    if num_table_dict.get(num_tables) is None:
        num_table_dict[num_tables] = 0
    
    num_table_dict[num_tables] += 1

    if num_footnotes_dict.get(num_footnotes) is None:
        num_footnotes_dict[num_footnotes] = 0

    num_footnotes_dict[num_footnotes] += 1

    total_tables += num_tables
    total_footnotes += num_footnotes
    total_references += num_references

sorted_dict_by_keys = dict(sorted(num_table_dict.items()))
sorted_footnotes_by_keys = dict(sorted(num_footnotes_dict.items()))

print(f"Total articles: {len(filenames)}")
print(f"Total tables: {total_tables}")
print(f"Articles with more references than the number of tables: {num_articles_extra_ref}")

print(sorted_dict_by_keys)
print('\n')
print(sorted_footnotes_by_keys)