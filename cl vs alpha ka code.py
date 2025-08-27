import csv
import os

# Folder paths
input_folder = 'E BACH GAYE ADITYA cl'
output_folder = 'output (E BACH GAYE ADITYA cl)'
os.makedirs(output_folder, exist_ok=True)

def is_float(value):
    try:
        float(value)
        return True
    except:
        return False

# Local max > 0, fallback to global max if > 0
def find_prominent_local_max(x_vals, y_vals):
    local_maxima = []
    for i in range(1, len(y_vals) - 1):
        if y_vals[i] > y_vals[i - 1] and y_vals[i] > y_vals[i + 1] and y_vals[i] > 0:
            local_maxima.append((y_vals[i], x_vals[i]))
    if local_maxima:
        return max(local_maxima, key=lambda tup: tup[0])
    else:
        max_val = max(y_vals)
        if max_val > 0:
            return max_val, x_vals[y_vals.index(max_val)]
        else:
            return None, None

def find_y_at_x0(x_vals, y_vals):
    closest_idx = min(range(len(x_vals)), key=lambda i: abs(x_vals[i]))
    return y_vals[closest_idx]

def find_x_at_y_near_zero(x_vals, y_vals):
    closest_idx = min(range(len(y_vals)), key=lambda i: abs(y_vals[i]))
    return x_vals[closest_idx]

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
            row += [''] * (num_cols - len(row))
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

    output_rows = [["Metric", "Local/Global Max (>0)", "X at Max", "Min Value", "X at Min", "Y at X=0", "X at Y near 0"]]

    for i in range(0, num_cols - 1, 3):
        x_idx = i
        y_idx = i + 1
        if y_idx >= num_cols:
            continue

        x_header = headers[x_idx].strip()
        y_header = headers[y_idx].strip()

        valid_rows = [row for row in data if row[x_idx] is not None and row[y_idx] is not None]
        if not valid_rows:
            continue

        x_vals = [row[x_idx] for row in valid_rows]
        y_vals = [row[y_idx] for row in valid_rows]

        local_max_val, x_at_max = find_prominent_local_max(x_vals, y_vals)
        if local_max_val is None:
            continue  # skip if even global max isn't > 0

        min_val = min(y_vals)
        x_at_min = x_vals[y_vals.index(min_val)]
        y_at_x0 = find_y_at_x0(x_vals, y_vals)
        x_at_y_near_zero = find_x_at_y_near_zero(x_vals, y_vals)

        output_rows.append([
            y_header,
            local_max_val,
            x_at_max,
            min_val,
            x_at_min,
            y_at_x0,
            x_at_y_near_zero
        ])

    with open(output_path, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(output_rows)

print("✅ All files processed. Output saved in:", output_folder)
