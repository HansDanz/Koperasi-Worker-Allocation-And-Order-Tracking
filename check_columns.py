
import pandas as pd
try:
    df = pd.read_excel(r"d:\GEO\Koperasi-Worker-Allocation-And-Order-Tracking\data\geo dummy -2.xlsx")
    print("Columns:", df.columns.tolist())
except Exception as e:
    print(f"Error: {e}")
