# Adds text strings from the file to csv translation table as originals with correct csv formating

# File paths — edit these if needed
INPUT_TEXT_FILE = "to_translation.txt"
OUTPUT_CSV_FILE = "translations.csv"

import csv

def append_lines_as_csv():
    # Open the text file for reading and the CSV for appending
    with open(INPUT_TEXT_FILE, 'r', encoding='utf-8') as txt_file, \
         open(OUTPUT_CSV_FILE, 'a', newline='', encoding='utf-8') as csv_file:
        
        writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        
        # For each non-empty line, strip newline and write as a single-field row
        for line in txt_file:
            text = line.rstrip('\n')
            if text:
                writer.writerow([text])

if __name__ == "__main__":
    append_lines_as_csv()
    print(f"Appended lines from '{INPUT_TEXT_FILE}' to '{OUTPUT_CSV_FILE}'.")

