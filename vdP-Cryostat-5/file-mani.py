from pathlib import Path

folder = Path("./Data-20262306")   # change this to your folder path

for file in folder.glob("*.txt"):
    file.unlink()
    print(f"Deleted: {file}")