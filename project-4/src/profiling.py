import pandas as pd
import json
import os

import paths

def create_profiling_pre_alignment(data):
    all_entries_name = []
    all_entries_value = []
    all_entries_metric = []
    profiling_df_dict = {}

    # Claims extractions
    for claim in data:
        for key, row in claim.items():
            for spec_key, spec in row['specifications'].items():
                all_entries_name.append({'Key': spec['name'], 'Count': 1})
                all_entries_value.append({'Key': spec['name'] + "::" + spec['value'], 'Count': 1})
            all_entries_metric.append({'Key': row['Measure'], 'Count': 1})

    profiling_df_name = pd.DataFrame(all_entries_name)
    profiling_df_value = pd.DataFrame(all_entries_value)
    profiling_df_metric = pd.DataFrame(all_entries_metric)
    
    # Group-by to manage duplicate
    profiling_df_dict['name'] = (profiling_df_name.groupby('Key').sum().reset_index())
    profiling_df_dict['value'] = (profiling_df_value.groupby('Key').sum().reset_index())
    profiling_df_dict['metric'] = (profiling_df_metric.groupby('Key').sum().reset_index())

    return profiling_df_dict


def create_profiling_post_alignment(alignment):
    all_entries_name = []
    all_entries_value = []
    all_entries_metric = []
    profiling_df_dict = {}

    # for faster access of values' names
    id2aligned_name = {}
    for old_key, value_list in alignment["aligned_names"].items():
        for value in value_list:
            id2aligned_name[value] = old_key

    # we loop through aligned names, values and metrics
    # for values, we also need to check what name they had in aligned names (we use a dict for _FAST_ access)
    for type in alignment:
        for value, ids in alignment[type].items():
                if type == "aligned_names":
                    all_entries_name.append({'Key': value, 'Count': len(ids)})
                elif type == "aligned_values":
                    for id in ids:
                        name = id2aligned_name[id]
                        all_entries_value.append({'Key': name + "::" + value, 'Count': 1})
                elif type == "aligned_metrics":
                    all_entries_metric.append({'Key': value, 'Count': len(ids)})

    profiling_df_name = pd.DataFrame(all_entries_name)
    profiling_df_value = pd.DataFrame(all_entries_value)
    profiling_df_metric = pd.DataFrame(all_entries_metric)
    
    # Group-by to manage duplicate
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

        # Load all claims
        all_data = load_json_files_from_directory(paths.CLAIMS)

        # Create profiling with pre-aligned values
        profiling_df_dict = create_profiling_pre_alignment(all_data)

        for key in profiling_df_dict:
            filename = paths.PROFILING + '/pre-alignment/' + key.upper() + '_PROFILING.csv'
            profiling_df_dict[key].to_csv(filename, index=False)

            print(f"- \033[32mPre-alignment Profiling CSV file saved as {filename}\033[0m\n")

        # Create profiling with post-aligned values
        with open(paths.ALIGNMENT + "/TEAM_FOREST_ALIGNMENT.json", 'r') as file:
            alignment = json.load(file)

        profiling_df_dict = create_profiling_post_alignment(alignment)

        for key in profiling_df_dict:
            filename = paths.PROFILING + '/post-alignment/' + key.upper() + '_PROFILING.csv'
            profiling_df_dict[key].to_csv(filename, index=False)

            print(f"- \033[32mPost-alignment Profiling CSV file saved as {filename}\033[0m\n")

    except Exception as e:
        print(f"\033[31mError during the process: {e}\033[0m\n")