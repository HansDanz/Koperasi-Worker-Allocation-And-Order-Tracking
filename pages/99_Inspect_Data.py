import streamlit as st
import pandas as pd

st.title("Data Inspector")

try:
    df = pd.read_excel(r"d:\GEO\Koperasi-Worker-Allocation-And-Order-Tracking\data\geo dummy -2.xlsx")
    st.write("Columns:")
    st.write(df.columns.tolist())
    st.write("First 5 rows:")
    st.dataframe(df)
except Exception as e:
    st.error(f"Error: {e}")
