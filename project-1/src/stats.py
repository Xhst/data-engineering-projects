import os
import json
import paths
from collections import defaultdict

def collect_stats(base_folder: str, folder: str, destination_folder: str) -> None:
    filenames = os.listdir(f"{base_folder}/{folder}")

    # Dictionaries to collect statistics
    papers_by_number_of_tables: dict[int, list[str]] = defaultdict(list)
    papers_by_number_of_references: dict[int, list[str]] = defaultdict(list)
    papers_by_number_of_footnotes: dict[int, list[str]] = defaultdict(list)

    paper_table_number_of_references: dict[int, dict[str, str]] = defaultdict(dict)

    paper_table_without_caption: dict[str, list[str]] = defaultdict(list)
    paper_table_without_references: dict[str, list[str]] = defaultdict(list)
    
    for filename in filenames:
        with open(f"{base_folder}/{folder}/{filename}", "r", encoding="utf-8") as jsonFile:
            file_content = jsonFile.read()
            try:
                paper_data = json.loads(file_content)
                paper_id = filename.replace('.json', '')
                
                # Initialize counters
                num_tables = 0
                num_references = 0
                num_footnotes = 0

                for table_id, table_data in paper_data.items():
                    num_tables += 1  # Count the table

                    # Extract details
                    caption = table_data.get('caption', '')
                    table = table_data.get('table', '')
                    footnotes = table_data.get('footnotes', [])
                    references = table_data.get('references', [])

                    # Track references and footnotes counts
                    num_footnotes += len(footnotes)
                    num_references += len(references)

                    # Check for tables without captions or references
                    if not caption:
                        paper_table_without_caption[paper_id].append(table_id)
                    if not references:
                        paper_table_without_references[paper_id].append(table_id)
                
                # Classify papers by their number of tables, references, and footnotes
                papers_by_number_of_tables[num_tables].append(paper_id)
                papers_by_number_of_references[num_references].append(paper_id)
                papers_by_number_of_footnotes[num_footnotes].append(paper_id)

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {filename}: {e}")
            except KeyError as e:
                print(f"KeyError accessing data in {filename}: {e}")
    
    # Output the stats to destination folder
    output_stats = {
        "papers_by_number_of_tables": dict(sorted(papers_by_number_of_tables.items())),
        "papers_by_number_of_references": dict(sorted(papers_by_number_of_references.items())),
        "papers_by_number_of_footnotes": dict(sorted(papers_by_number_of_footnotes.items())),
        "paper_table_number_of_references": dict(sorted(paper_table_number_of_references.items())),
        "paper_table_without_caption": dict(sorted(paper_table_without_caption.items())),
        "paper_table_without_references": dict(sorted(paper_table_without_references.items())),
    }

    output_file = f"{destination_folder}/{folder}_stats.json"
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(output_stats, outfile, indent=4)
    print(f"Stats collected and saved to {output_file}")


def collect_tables_by_type(base_folder: str, folder: str, destination_folder: str) -> None:
    tables_by_type: dict[str, list[str]] = defaultdict(list)

    filenames = os.listdir(f"{base_folder}/{folder}")
    
    for filename in filenames:
        with open(f"{base_folder}/{folder}/{filename}", "r", encoding="utf-8") as jsonFile:
            file_content = jsonFile.read()
            ids: list[str] = json.loads(file_content)

            filename = filename.replace('.json', '')
            
            for id in ids:
                if ".T" in id:
                    tables_by_type['table'].append(f'{filename}@{id}')
                elif ".F" in id:
                    tables_by_type['figure'].append(f'{filename}@{id}')
                elif ".E" in id:
                    tables_by_type['equation'].append(f'{filename}@{id}')
                elif "example" in id.lower():
                    tables_by_type['example'].append(f'{filename}@{id}')
                elif "alg" in id.lower():
                    tables_by_type['algorithm'].append(f'{filename}@{id}')
                else:
                    tables_by_type['unknown'].append(f'{filename}@{id}')


    output_stats = {
        "tables_by_type": dict(sorted(tables_by_type.items())),
    }

    output_file = f"{destination_folder}/tables_by_type_stats.json"
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(output_stats, outfile, indent=4)


if __name__ == "__main__":
    json_folder = paths.JSON_FOLDER
    stats_folder = paths.STATS_FOLDER

    if not os.path.exists(stats_folder):
        os.makedirs(stats_folder)

    extract_folders = ['simple_forward_extractor', 'forward_extractor', 'backward_extractor']

    for folder in extract_folders:
        extract_folder = f"{json_folder}/{folder}"

        collect_stats(json_folder, folder, stats_folder)
    
    collect_tables_by_type(json_folder, 'all_tags', stats_folder)

        
                
                

