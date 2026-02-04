# Translate the first column of csv as original to languages from header by language code

# Dependencies installation
# pip install googletrans==4.0.0-rc1

import asyncio
import csv
from googletrans import Translator


# -------------------------
# Configuration
# -------------------------

INPUT_FILE_PATH = "translations.csv"
OUTPUT_FILE_PATH = "translations_out.csv"

CSV_DELIMITER = ";"  # <-- change this to "," or ";" as needed

START_LINE_ABS = 1
END_LINE_ABS = 64
IS_WRITE_SKIPPED_ROWS = True

SKIP_LANGUAGES = ["", "original", "emoji", "en"]


# -------------------------
# Open files
# -------------------------

infile = open(INPUT_FILE_PATH, encoding="utf-8", newline="")
outfile = open(OUTPUT_FILE_PATH, "w", encoding="utf-8", newline="")

reader = csv.reader(infile, delimiter=CSV_DELIMITER)
writer = csv.writer(
	outfile,
	delimiter=CSV_DELIMITER,
	quoting=csv.QUOTE_MINIMAL
)

# Transfer header
header = next(reader)
writer.writerow(header)


# -------------------------
# Main logic
# -------------------------

async def main():
	translator = Translator()

	print(f"Header: {header}")

	row_number = 0
	for row in reader:
		row_number += 1
		absolute_row = row_number + 1

		# Skip conditions
		if (
			absolute_row < START_LINE_ABS or
			absolute_row > END_LINE_ABS or
			len(row) < 1 or
			row[0] == ""
		):
			if IS_WRITE_SKIPPED_ROWS:
				writer.writerow(row)
			continue

		# Original text
		orig = row[0].replace("\\n", "\n")

		for language_number, language in enumerate(header):
			print(f"Process language [{language}] for row [{absolute_row}]")

			# Skip original / excluded languages
			if language in SKIP_LANGUAGES:
				if language_number != 0:
					_ensure_row_length(row, language_number)
					row[language_number] = ""
				continue

			# Translate
			translated = await translator.translate(
				orig,
				src="en",
				dest=language
			)

			text = translated.text.replace("\n", "\\n")

			_ensure_row_length(row, language_number)
			row[language_number] = text

		writer.writerow(row)


def _ensure_row_length(row, index):
	while len(row) <= index:
		row.append("")


# -------------------------
# Run
# -------------------------

asyncio.run(main())
