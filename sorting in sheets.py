import os
import csv
import xlsxwriter

input_folder = 'outputs E BACH GAYE ADITYA'
output_folder = 'grouped_outputs E BACH GAYE ADITYA'
os.makedirs(output_folder, exist_ok=True)

# Define RE groups to search for
re_tags = ['150', '250']

# Loop through each clean CSV
for filename in os.listdir(input_folder):
    if not filename.endswith('_clean.csv'):
        continue

    input_path = os.path.join(input_folder, filename)
    base_name = os.path.splitext(filename)[0].replace('_clean', '')
    output_path = os.path.join(output_folder, f'{base_name}_grouped.xlsx')

    # Initialize grouped rows
    grouped_rows = {tag: [] for tag in re_tags}
    headers = []

    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)  # read header

        for row in reader:
            metric = row[0]
            for tag in re_tags:
                if tag in metric:
                    grouped_rows[tag].append(row)
                    break  # Avoid duplicate tagging

    # Write to Excel with xlsxwriter
    workbook = xlsxwriter.Workbook(output_path)
    for tag in re_tags:
        rows = grouped_rows[tag]
        if not rows:
            continue

        sheet_name = f"RE{tag.replace('_','_')}"
        worksheet = workbook.add_worksheet(sheet_name)

        # Write headers
        for col_idx, val in enumerate(headers):
            worksheet.write(0, col_idx, val)

        # Write rows
        for row_idx, row in enumerate(rows, start=1):
            for col_idx, val in enumerate(row):
                worksheet.write(row_idx, col_idx, val)

    workbook.close()

print("✅ Excel files with RE-grouped sheets saved in 'grouped_excel_outputs/' folder.")
