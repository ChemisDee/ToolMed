
import streamlit as st
import pandas as pd
from rapidfuzz import fuzz

st.set_page_config(page_title="Excel Price Summation", layout="centered")
st.title("📊 Excel Price Summation Tool")

def normalize(text):
    return str(text).strip().lower() if pd.notna(text) else ""

def fuzzy_match(needle, haystack_list, threshold=85):
    return any(fuzz.ratio(needle, item) >= threshold for item in haystack_list)

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if not {'Name', 'Synonym', 'Price'}.issubset(df.columns):
            st.error("Excel must contain 'Name', 'Synonym', and 'Price' columns.")
        else:
            st.success("File uploaded successfully!")
            st.write("Preview:", df.head())

            df["Name_norm"] = df["Name"].apply(normalize)
            df["Synonym_norm"] = df["Synonym"].apply(normalize)

            input_text = st.text_input("Enter names or synonyms (comma-separated):")

            if input_text:
                entries = [normalize(e) for e in input_text.split(",") if e.strip()]
                matched_rows = []

                for _, row in df.iterrows():
                    haystack = [row["Name_norm"], row["Synonym_norm"]]
                    if any(fuzzy_match(entry, haystack) for entry in entries):
                        matched_rows.append(row)

                if matched_rows:
                    matched_df = pd.DataFrame(matched_rows)
                    total = matched_df["Price"].sum()
                    st.write("### ✅ Matched Entries")
                    st.dataframe(matched_df[["Name", "Synonym", "Price"]])
                    st.success(f"💰 Total Price: {total:.2f}")
                else:
                    st.warning("No matching entries found.")

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
