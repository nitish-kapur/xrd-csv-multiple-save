# XRD Plotter from CSV (Multiple Save)

A Python script that batch processes XRD diffraction patterns from CSV files and saves individual plots as high-resolution PNG images.

## Author

**Nitish Kapur**<br>
GitHub: [github.com/nitish-kapur](https://github.com/nitish-kapur)

## Expected Input Format

The script expects CSV files exported from an XRD instrument. Each file must contain a `[Scan points]` section marker, after which the diffraction data begins in at least three comma-separated columns:

    ... (metadata — instrument name, date, settings, etc.) ...
    [Scan points]
    0.020, 0.5, 123.0
    0.040, 0.5, 145.0
    0.060, 0.5, 132.0
    ...

- Three columns are expected per data row as this matches the fixed export format of the XRD instrument. Only columns 1 and 3 are plotted; column 2 (time per step) is read but discarded.

| Element | Description |
|---|---|
| Metadata lines | Any number of lines before `[Scan points]` — automatically ignored by the parser |
| `[Scan points]` marker | Signals the end of metadata; data parsing begins on the next line |
| Column 1 | 2-Theta angle (°) — numeric float, plotted on X-axis |
| Column 2 | Time per step — present in the file but not plotted |
| Column 3 | Intensity (counts) — numeric float, plotted on Y-axis |
| Separator | Comma (`,`) |
| Empty lines | Skipped automatically |
| Malformed lines | Lines with fewer than three values are skipped with a console warning |

## Requirements

    pip install pandas matplotlib

## Configuration

The input and output folder paths are hard-coded at the top of the script. Update these to match your directory structure:

    desktop_path  = r"F:\"
    input_folder  = os.path.join(desktop_path, "raw")   # Folder containing CSV files
    output_folder = os.path.join(desktop_path, "nk")    # Folder to save PNG plots

## Usage

1. Place all XRD CSV files in the input folder
2. Run:

    python xrd-csv-multiple-save.py

Plots are saved automatically to the output folder with a timestamp appended to each filename.

## Output

| File | Description |
|---|---|
| `<filename>_<timestamp>_XRD.png` | High-resolution plot (300 dpi) saved in the output folder |

## Notes

- Files that do not contain a `[Scan points]` marker or have no valid data are skipped automatically.
- The output folder is created automatically if it does not exist.
- Each plot is saved and closed immediately to conserve memory when processing large batches.
