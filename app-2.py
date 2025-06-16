import streamlit as st
import pandas as pd
from matcher import get_fuzzy_matches

st.set_page_config(page_title="Excel Price Summation", layout="centered")
st.title("📊 Excel Price Summation Tool")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if not {'Name', 'Synonym', 'Price'}.issubset(df.columns):
            st.error("Excel must contain 'Name', 'Synonym', and 'Price' columns.")
        else:
            st.success("File uploaded successfully!")
            st.write("Preview:", df.head())

            input_text = st.text_input("Enter names or synonyms (comma-separated):")

            if input_text:
                matched_df = get_fuzzy_matches(df, input_text)

                if matched_df.empty:
                    st.warning("No matching entries found.")
                else:
                    # Allow users to remove specific rows
                    display_labels = matched_df["Name"] + " (" + matched_df["Synonym"] + ")"
                    to_remove = st.multiselect("❌ Remove entries you didn't mean:", display_labels)

                    filtered_df = matched_df[~display_labels.isin(to_remove)]
                    total = filtered_df["Price"].sum()

                    st.write("### ✅ Final Selected Entries")
                    st.dataframe(filtered_df[["Name", "Synonym", "Price"]])
                    st.success(f"💰 Total Price after removal: {total:.2f}")

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")

DEFAULT_FILE = "DefaultPreise.xlsx"

# Try to use uploaded file, otherwise fall back to default
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("Custom file loaded.")
else:
    df = pd.read_excel(DEFAULT_FILE)
    st.info("Using built-in price list from repository.")
