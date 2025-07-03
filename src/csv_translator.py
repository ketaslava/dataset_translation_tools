# Dependencies installation
# pip install googletrans


# Imports
import asyncio
from googletrans import Translator
import csv


# Configuration
START_LINE_ABS = 60
END_LINE_ABS = 60
IS_WRITE_SKIPPED_ROWS = True
SKIP_LANGUAGES = ["", "original", "emoji"]


# Open files
infile = open('translations.csv', encoding='utf-8')
outfile = open('translations_out.csv', 'w', encoding='utf-8', newline='')


# Transfer header
reader = csv.reader(infile)
writer = csv.writer(outfile)
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
		
		# Row skipping
		if (row_number + 1 < START_LINE_ABS) or \
				(row_number + 1 > END_LINE_ABS):
			if IS_WRITE_SKIPPED_ROWS:
				writer.writerow(row)
			continue
		
		# Get original
		orig = row[0]
		
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
			
			# Write to the row
			if len(row) <= language_number:
				row.append(text)
			else:
				row[language_number] = text
			
		# Write the row
		writer.writerow(row)


# Run main process
asyncio.run(main())
