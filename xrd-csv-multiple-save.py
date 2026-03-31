"""
XRD Plotter from CSV (Multiple Save)
Copyright (C) 2026 Nitish Kapur
GitHub: github.com/nitish-kapur
Licensed under GNU GPLv3

    This script was made as a part of a biofuel research project.

    1.  Scans the input folder for all CSV files exported from an XRD
        instrument. Update the input_path, input_folder, and
        output_folder variables at the top of the script to match your
        directory structure.

    2.  For each CSV file, reads all lines and locates the [Scan points]
        section marker to identify where the diffraction data begins. All
        metadata lines above [Scan points] (instrument name, date,
        settings, etc.) are automatically ignored. Files without this
        marker are skipped.

    3.  Expected data format after the [Scan points] marker:

            ... (metadata — instrument name, date, settings, etc.) ...
            [Scan points]
            0.020, 0.5, 123.0
            0.040, 0.5, 145.0
            ...     ...    ...

            i.e.,
                Element         Description
                -----------     --------------------------------------------------
                Column 1        2-Theta angle (°) — numeric float, plotted on X-axis
                Column 2        Time per step — present in file but not plotted
                Column 3        Intensity (counts) — numeric float, plotted on Y-axis
                Separator       Comma (,)
                Empty lines     Skipped automatically
                Malformed lines Skipped with a console warning

        Note: Three columns are required per row as this matches the fixed
        export format of the XRD instrument. Only columns 1 and 3 are
        plotted; column 2 is read solely to validate the row structure.

    4.  Loads the parsed data into a pandas DataFrame and generates a
        matplotlib line plot for each file with:
            - X-axis: 2-Theta (°)
            - Y-axis: Intensity (counts)
            - Title: derived from the CSV filename

    5.  Saves each plot as a timestamped high-resolution PNG (300 dpi)
        in the output folder. The output folder is created automatically
        if it does not exist.

    6.  Reports the number of successfully processed files to the console
        upon completion.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- Paths ---
input_path = r"F:\"
input_folder = os.path.join(input_path, "raw")  
output_folder = os.path.join(input_path, "nk")  
os.makedirs(output_folder, exist_ok=True)

# --- Timestamp for filenames ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

files_processed = 0

for filename in sorted(os.listdir(input_folder)):
    if filename.lower().endswith(".csv"):
        print(f"Processing file: {filename}")
        file_path = os.path.join(input_folder, filename)

        # Read the entire file as lines
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Find the start of the [Scan points] section (case-insensitive)
        data_start_index = None
        for i, line in enumerate(lines):
            if "[scan points]" in line.lower():
                data_start_index = i + 1
                break

        if data_start_index is None:
            print(f"No [Scan points] section found in {filename}, skipping.")
            continue

        # Extract scan points data lines
        data_lines = lines[data_start_index:]

        parsed_data = []
        for line in data_lines:
            line = line.strip()
            if not line:
                continue  # skip empty lines
            parts = line.split(',')
            # At least 3 columns (Angle, TimePerStep, Intensity) are expected
            if len(parts) >= 3:
                try:
                    angle = float(parts[0].strip())
                    intensity = float(parts[2].strip())
                    parsed_data.append([angle, intensity])
                except ValueError:
                    print(f"Skipping non-numeric line in {filename}: {line}")
            else:
                print(f"Skipping malformed line in {filename}: {line}")

        if not parsed_data:
            print(f"No valid XRD data found in {filename}, skipping.")
            continue

        files_processed += 1

        # Create DataFrame for plotting
        df = pd.DataFrame(parsed_data, columns=["Angle", "Intensity"])

        # Prepare plot
        plt.figure(figsize=(10, 5))
        plt.plot(df["Angle"], df["Intensity"], color='blue', linewidth=1)
        plt.title(f"{os.path.splitext(filename)[0]} - XRD Pattern")
        plt.xlabel("2 Theta (°)")
        plt.ylabel("Intensity (counts)")
        plt.grid(True)
        plt.tight_layout()

        # Save plot with timestamp
        save_filename = f"{os.path.splitext(filename)[0]}_{timestamp}_XRD.png"
        save_path = os.path.join(output_folder, save_filename)
        plt.savefig(save_path, dpi=300)
        plt.close()

        print(f"Saved XRD plot for {filename} as {save_filename}")

if files_processed == 0:
    print("No CSV files found or no valid XRD data processed.")
else:
    print(f"Processed and saved XRD plots for {files_processed} files.")
