# Removes texts from the file from translations csv table

# File paths — edit these if needed
INPUT_TEXT_FILE = "to_remove.txt"
TRANSLATION_CSV_FILE = "translations.csv"

import csv

def remove_translations():
    # 1. Read the list of keys to remove (strip newline, skip blanks)
    with open(INPUT_TEXT_FILE, 'r', encoding='utf-8') as f:
        keys_to_remove = {line.rstrip('\n') for line in f if line.strip()}
    
    # 2. Load all rows from the CSV
    with open(TRANSLATION_CSV_FILE, 'r', encoding='utf-8', newline='') as csv_in:
        reader = csv.reader(csv_in)
        rows = list(reader)
    
    # 3. Separate header and data rows
    header, data_rows = rows[0], rows[1:]
    
    # 4. Keep only rows whose key (first column) is NOT in keys_to_remove
    filtered_rows = [row for row in data_rows if row and row[0] not in keys_to_remove]
    
    # 5. Overwrite the CSV with header + filtered rows
    with open(TRANSLATION_CSV_FILE, 'w', encoding='utf-8', newline='') as csv_out:
        writer = csv.writer(csv_out, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        writer.writerows(filtered_rows)

if __name__ == "__main__":
    remove_translations()
    print(f"Removed entries from '{TRANSLATION_CSV_FILE}' matching lines in '{INPUT_TEXT_FILE}'.")

