# Translate the first column of csv as original to languages from header by language code


# Dependencies installation
# pip install googletrans


# Imports
import asyncio
from googletrans import Translator
import csv


# Configuration
INPUT_FILE_PATH = "translations.csv"
OUTPUT_FILE_PATH = "translations_out.csv"
START_LINE_ABS = 1
END_LINE_ABS = 64
IS_WRITE_SKIPPED_ROWS = True
SKIP_LANGUAGES = ["", "original", "emoji"]


# Open files
infile = open(INPUT_FILE_PATH, encoding='utf-8')
outfile = open(OUTPUT_FILE_PATH, 'w', encoding='utf-8', newline='')


# Transfer header
reader = csv.reader(infile)
writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
header = next(reader)
writer.writerow(header)


# Main
async def main():
	translator = Translator()
	
	print(f"Header: {header}]")
	
	# return
	
	# Next row
	row_number = 0
	for row in reader:
		row_number += 1
		
		# Row skipping by selection and by emptyness
		if (row_number + 1 < START_LINE_ABS) or \
				(row_number + 1 > END_LINE_ABS) or \
				(len(row) < 1) or (row[0] == ""):
			if IS_WRITE_SKIPPED_ROWS:
				writer.writerow(row)
			continue
		
		# Get original
		orig = row[0]
		
		# Desanitize original
		orig = orig.replace("\\n", "\n")
		
		# Translate to next language
		language_number = -1
		for language in header:
			language_number += 1
			
			# Log
			print(f"Process language [{language}] for row [{row_number+1}]")
			
			# Skip original
			if language in SKIP_LANGUAGES:
				# Place empty string in all cases except for skipping original 
				if language_number != 0:
					if len(row) <= language_number:
						row.append("")
					else:
						row[language_number] = ""
				# Go next
				continue
			
			# Translete
			translated = await translator.translate(orig, src='en', dest=language)
			text = translated.text
			
			# Sanitize translation original
			text = text.replace("\n", "\\n")
			
			# Write to the row
			if len(row) <= language_number:
				row.append(text)
			else:
				row[language_number] = text
			
		# Write the row
		writer.writerow(row)


# Run main process
asyncio.run(main())
