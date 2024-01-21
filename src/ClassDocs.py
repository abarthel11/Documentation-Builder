import os
import re
import csv

def extract_annotations(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # Extract @author and @description annotations
        author_match = re.search(r'@author\s+(.*?$)', content, re.MULTILINE)
        description_match = re.search(r'@description\s+(.*?$)', content, re.MULTILINE)

        author = author_match.group(1) if author_match else ''
        description = description_match.group(1) if description_match else ''

        # Extract the entire modifications log section
        modifications_log_match = re.search(r'\bModifications Log\b(.*?)(?=\n\s*\n|\Z)', content, re.DOTALL | re.MULTILINE)
        modifications_log = modifications_log_match.group(1).strip() if modifications_log_match else ''

        # Extract the last entry in the modifications log
        last_modification_match = re.findall(r'\b(\d+\.\d+)\s+(\d{2}-\d{2}-\d{4})\s+(.*?)\s+(.*?)\s*$', modifications_log, re.MULTILINE)
        last_modification = last_modification_match[-1] if last_modification_match else ('', '', '', '')

        return author, description, last_modification

def process_files(file_paths):
    data = []
    for file_path in file_paths:
        author, description, (version, date, mod_author, modification) = extract_annotations(file_path)
        data.append([os.path.basename(file_path), author, description, version, date, mod_author, modification])

    return data

def create_document(file_paths):
    table_data = process_files(file_paths)

    headers = ['File Name', 'Author', 'Description', 'Version', 'Date', 'Mod Author', 'Last Modification']

    with open('./output/CloudCoachClasses.csv', 'w', encoding='utf-8', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(table_data)

if __name__ == "__main__":
    # Replace 'your_directory_path' with the path to your list of files
    directory_path = './input/force-app/main/default/classes'
    
    # List all files in the directory with .cls extension (you can modify it based on your file types)
    file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.cls')]

    create_document(file_paths)
