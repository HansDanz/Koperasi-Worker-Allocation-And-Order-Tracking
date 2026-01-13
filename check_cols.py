import pandas as pd
try:
    df = pd.read_excel(r"d:\GEO\Koperasi-Worker-Allocation-And-Order-Tracking\data\geo dummy -2.xlsx")
    with open("cols.txt", "w") as f:
        f.write("\n".join(df.columns.astype(str)))
except Exception as e:
    with open("cols.txt", "w") as f:
        f.write(str(e))
