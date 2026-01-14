
import pandas as pd

try:
    df = pd.read_excel(r'd:\GEO\Koperasi-Worker-Allocation-And-Order-Tracking\data\geo dummy -2.xlsx')
    print("Columns:", df.columns.tolist())
    print("First few rows of 'Specialist' column if it exists:")
    if 'Specialist' in df.columns:
        print(df['Specialist'].head())
    else:
        print("'Specialist' column not found.")
except Exception as e:
    print(e)
