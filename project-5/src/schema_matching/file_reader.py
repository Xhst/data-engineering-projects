import pandas as pd

def read_file(file_path: str) -> pd.DataFrame:
    """
    Read a file and return the data as a pandas DataFrame
    
    Args:
        file_path (str): The path to the file to be read

    Returns:
        pd.DataFrame: The data in the file as a pandas DataFrame
    """

    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        elif file_path.endswith('.json'):
            return pd.read_json(file_path)
        elif file_path.endswith('.jsonl'):
            return pd.read_json(file_path, lines=True)
        else:
            raise ValueError("File format not supported")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

