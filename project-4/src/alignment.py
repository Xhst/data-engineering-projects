import json
import os
from collections import defaultdict

import paths

def from_dict_to_json(alignment_dict, data_name):
    data = {
    data_name: alignment_dict
    }

    file_path = f"{paths.ALIGNMENT}/{data_name}_ALIGNMENT.json"

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"\n\033[32mSalvato in {file_path}\033[0m\n")    


def create_alignment(directory_path):

    alignment_names_df_dict = defaultdict(list)
    alignment_values_df_dict = defaultdict(list)

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)

                f_name = filename.rstrip('claims.json')

                for claim in data:
                    for key, row in claim.items():
                        for spec_key, spec in row['specifications'].items():
                            alignment_names_df_dict[spec['name']].append(f"{f_name}{key}_{spec_key}")
                            alignment_values_df_dict[spec['value']].append(f"{f_name}{key}_{spec_key}")

    from_dict_to_json(alignment_names_df_dict, "aligned_names")
    from_dict_to_json(alignment_values_df_dict, "aligned_values")



if __name__ == "__main__":

    if not os.path.exists(paths.ALIGNMENT):
        os.makedirs(paths.ALIGNMENT)
        print(f"\n\033[32mCreated directory: {paths.ALIGNMENT}\033[0m\n")
        
    create_alignment(paths.CLAIMS)