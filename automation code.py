import csv
import os

# Folder paths
input_folder = 'E BACH GAYE ADITYA'
output_folder = 'outputs E BACH GAYE ADITYA'
os.makedirs(output_folder, exist_ok=True)

def is_float(value):
    try:
        float(value)
        return True
    except:
        return False

# Process each CSV file
for filename in os.listdir(input_folder):
    if not filename.endswith('.csv'):
        continue

    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_clean.csv")

    with open(input_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        num_cols = len(headers)

        data = []
        for row in reader:
            row += [''] * (num_cols - len(row))  # pad
            if all(cell.strip() == '' for cell in row):
                continue
            cleaned = []
            for val in row:
                val = val.strip()
                if is_float(val):
                    cleaned.append(float(val))
                else:
                    cleaned.append(None)
            data.append(cleaned)

    # Create clean rows for output
    output_rows = []
    output_rows.append(["Metric", "Max Value", "X at Max", "Min Value", "X at Min"])

    for i in range(0, num_cols - 1, 3):  # step by 3: X, Y, blank
        x_idx = i
        y_idx = i + 1
        if y_idx >= num_cols:
            continue

        x_header = headers[x_idx].strip()
        y_header = headers[y_idx].strip()

        valid_rows = [
            row for row in data
            if row[x_idx] is not None and row[y_idx] is not None
        ]
        if not valid_rows:
            continue

        x_vals = [row[x_idx] for row in valid_rows]
        y_vals = [row[y_idx] for row in valid_rows]

        max_val = max(y_vals)
        max_idx = y_vals.index(max_val)
        x_at_max = x_vals[max_idx]

        min_val = min(y_vals)
        min_idx = y_vals.index(min_val)
        x_at_min = x_vals[min_idx]

        output_rows.append([y_header, max_val, x_at_max, min_val, x_at_min])

    # Write to new structured CSV
    with open(output_path, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(output_rows)

print("✅ Output files created with 5-column format in the 'outputs/' folder.")
