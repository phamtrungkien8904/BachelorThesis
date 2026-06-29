from pathlib import Path

# Folder containing the files.
# Use Path.cwd() if the script is placed inside that folder.
folder = Path.cwd()

prefix = "202605090"
allowed_extensions = {".dat", ".txt", ".wrn", ".log", ".csv", ".xml"}

for file_path in folder.iterdir():
    if not file_path.is_file():
        continue

    # Only rename files with allowed extensions
    if file_path.suffix.lower() not in allowed_extensions:
        continue

    # Only rename files whose names are numbers, such as 01.dat
    if not file_path.stem.isdigit():
        continue

    new_name = prefix + file_path.name
    new_path = file_path.with_name(new_name)

    if new_path.exists():
        print(f"Skipped because destination already exists: {new_path.name}")
        continue

    file_path.rename(new_path)
    print(f"Renamed: {file_path.name} -> {new_path.name}")