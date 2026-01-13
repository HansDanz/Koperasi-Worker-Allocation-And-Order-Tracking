import pandas as pd

try:
    df = pd.read_excel(r"d:\GEO\Koperasi-Worker-Allocation-And-Order-Tracking\data\geo dummy -2.xlsx")
    print("Columns:", df.columns.tolist())
    print("\nFirst 3 rows:")
    print(df.head(3).to_string())
except Exception as e:
    print("Error reading excel:", e)
    # Try installing openpyxl if meant to be run in env that lacks it (though user env has pandas, openpyxl usually needed for xlsx)
