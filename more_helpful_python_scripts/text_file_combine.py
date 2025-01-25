# path: flask_app/app/static/annotation_text_files/*
import os

def combine_sorted_text_files(input_dir, output_file):
    all_lines = []

    # Read all lines from all text files in the directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):  # Only process text files
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r') as infile:
                all_lines.extend(infile.readlines())  # Collect all lines into a list

    # Sort the lines by the first column
    all_lines.sort(key=lambda line: line.split()[0] if line.strip() else "")  # Sort by the first word/column

    # Write the sorted lines to the output file
    with open(output_file, 'w') as outfile:
        outfile.writelines(all_lines)
if __name__ == "__main__":
    input_directory = "app/static/annotation_text_files"
    output_file_name = "combined_annotation_files.txt"
    combine_sorted_text_files(input_directory, output_file_name)