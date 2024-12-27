from file_reader import read_file
import os
import json
import pandas as pd

SOURCES_FOLDER = '../../sources'
OUTPUT_FILE = './mediated_schema/aggregated_sources.csv'

def load_sources_dataframes(sources_folder: str) -> dict:
    """
    Load the data from the sources folder into a dictionary of DataFrames.
    
    Args:
        sources_folder (str): The path to the folder containing the source files.
    
    Returns:
        dict: A dictionary containing the data from the source files as DataFrames.
    """
    sources_data = {}

    for folder in os.listdir(sources_folder):
        folder_path = os.path.join(sources_folder, folder)
        if os.path.isdir(folder_path):
            sources_data[folder] = {}
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    sources_data[folder][file] = read_file(file_path)
    
    return sources_data

if __name__ == '__main__':
    sources_data = load_sources_dataframes(SOURCES_FOLDER)

    # Load the mediated schema mapping
    with open('./mediated_schema/schema_mapping.json', 'r') as file:
        mapping = json.load(file)

    # Initialize an empty DataFrame
    aggregated_df = pd.DataFrame()

    for source, data in sources_data.items():

        for file, df in data.items():

            if df is None:
                print(f'Dataframe missing for {file}')
                continue

            # Create a mapping for the current source and mediated schema
            column_mapping = {}
            for col_name in df.columns:
                field_str = f"{source}__{file}__{col_name}"

                for ms_field, mapped_fields in mapping.items():

                    if field_str in mapped_fields:
                        column_mapping[col_name] = ms_field
                        print(f"Mapping {field_str} to {ms_field}")
                        break

            # Filter and rename the DataFrame to match the mediated schema
            filtered_df = df[column_mapping.keys()].rename(columns=column_mapping)

            # Append to the aggregated DataFrame
            aggregated_df = pd.concat([aggregated_df, filtered_df], ignore_index=True)

    # Reorder columns to match the mediated schema, filling missing columns with NaN
    aggregated_df = aggregated_df.reindex(columns=mapping.keys())

    # Save the aggregated DataFrame to a CSV
    aggregated_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Aggregated data saved to {OUTPUT_FILE}")
