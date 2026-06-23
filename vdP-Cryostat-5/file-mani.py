from pathlib import Path

folder = Path("./Data-20261006")   # change this to your folder path

for file in folder.glob("*.txt"):
    file.unlink()
    print(f"Deleted: {file}")