import os

def extract_new_file_name(file_name):
    """
    Extract a new file name based on the specified rules.
    """

    # Check and extract based on patterns
    if "arXiv_" in file_name:
        return file_name.split("arXiv_")[-1]
    elif "arXiv" in file_name:
        return file_name.split("arXiv")[-1]
    elif "ar5iv_article_" in file_name:
        return file_name.split("ar5iv_article_")[-1]
    
    return file_name

def rename_files_in_directory(directory_path):
    """
    Rename files in the specified directory according to the rules.
    """
    try:
        for file_name in os.listdir(directory_path):
            old_file_path = os.path.join(directory_path, file_name)

            # Skip if not a file
            if not os.path.isfile(old_file_path):
                continue

            # Generate new file name
            new_file_name = extract_new_file_name(file_name)
            new_file_path = os.path.join(directory_path, new_file_name)

            # Rename the file
            try:
                os.rename(old_file_path, new_file_path)
            except Exception as e:
                print(f"Duplicate: {new_file_name}")
                os.remove(old_file_path)
                
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Input the directory path
    directory_path = "server/target/sources/html"
    rename_files_in_directory(directory_path)