import pandas as pd
import json
import os

import paths

def create_profiling(data):

    all_entries_name = []
    all_entries_value = []
    all_entries_metric = []
    profiling_df_dict = {}

    # Claims extractions
    for claim in data:
        for spec in claim['Specifications']:
            all_entries_name.append({'Key': spec['name'], 'Count': 1})
            all_entries_value.append({'Key': spec['value'], 'Count': 1})
        all_entries_metric.append({'Key': claim['Measure'], 'Count': 1})


    profiling_df_name = pd.DataFrame(all_entries_name)
    profiling_df_value = pd.DataFrame(all_entries_value)
    profiling_df_metric = pd.DataFrame(all_entries_metric)
    
    # Remove duplicate
    profiling_df_dict['name'] = (profiling_df_name.groupby('Key').sum().reset_index())
    profiling_df_dict['value'] = (profiling_df_value.groupby('Key').sum().reset_index())
    profiling_df_dict['metric'] = (profiling_df_metric.groupby('Key').sum().reset_index())

    return profiling_df_dict

def load_json_files_from_directory(directory_path):
    all_data = [] 

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                all_data.extend(data) 
    return all_data


if __name__ == "__main__":

    try:
        if not os.path.exists(paths.PROFILING):
            os.makedirs(paths.PROFILING)
            print(f"\033[32mCreated directory: {paths.PROFILING}\033[0m\n")

        # Carica i dati da tutti i file JSON nella cartella
        all_data = load_json_files_from_directory(paths.CLAIMS)

        # Calcolo della profilazione
        profiling_df_dict = create_profiling(all_data)

        for key in profiling_df_dict:

            filename = paths.PROFILING + '/' + key + '_profiling.csv'
            profiling_df_dict[key].to_csv(filename, index=False)

            print(f"- \033[32mProfiling CSV file saved as {filename}\033[0m\n")

    except Exception as e:
        print(f"\033[31mError during the process: {e}\033[0m\n")