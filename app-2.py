import streamlit as st
import pandas as pd
from matcher import get_fuzzy_matches

st.set_page_config(page_title="Excel Price Summation", layout="centered")
st.title("Rechner für Kostenanfragen")

DEFAULT_FILE = "DefaultPreise.xlsx"

# One file_uploader, fallback if nothing is uploaded
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])
use_default = False

try:
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.success("Eigene Preisliste wird verwendet.")
 
    else:
        df = pd.read_excel(DEFAULT_FILE)
        st.info("Standardpreisliste wird verwendet.")
        use_default = True

    if not {'Name', 'Synonym', 'Price'}.issubset(df.columns):
        st.error("Excel must contain 'Name', 'Synonym', and 'Price' columns.")
    else:
        input_text = st.text_input("Analysekürzel oder -namen eingeben und durch Kommata separieren (bspw. TSH, Vitamin D, ...):")

        if input_text:
            matched_df = get_fuzzy_matches(df, input_text)

            if matched_df.empty:
                st.warning("No matching entries found.")
            else:
                display_labels = matched_df["Name"] + " (" + matched_df["Synonym"] + ")"
                to_remove = st.multiselect("❌ Remove entries you didn't mean:", display_labels)

                filtered_df = matched_df[~display_labels.isin(to_remove)]
                total = filtered_df["Price"].sum()

                st.write("### ✅ Final Selected Entries")
                st.dataframe(filtered_df[["Name", "Synonym", "Price"]])
                st.success(f"💰 Total Price after removal: {total:.2f}")

                # Get normalized user inputs
                entries = [entry.strip().lower() for entry in input_text.split(",") if entry.strip()]

                # Get all matched synonyms and names
                matched_terms = set()
                for _, row in matched_df.iterrows():
                    matched_terms.add(row["Name"].strip().lower())
                    matched_terms.update([s.strip().lower() for s in str(row["Synonym"]).split(",")])

                # Find unmatched entries
                unmatched = [e for e in entries if not any(e in matched for matched in matched_terms)]

                if unmatched:
                    st.markdown("### ⚠️ Nicht gefundene Eingaben")
                    st.warning(f"Die folgenden Begriffe konnten nicht zugeordnet werden: {', '.join(unmatched)}")

                email_text = f"""Guten Tag,

Vielen Dank für Ihre Anfrage. Die Kosten für die von Ihnen gewünschten Analysen belaufen sich total auf {total:.2f} CHF (Angaben ohne Gewähr).

Freundliche Grüsse,
"""

                st.markdown("### ✉️ Vorschlag für Antwort-E-Mail")
                st.text_area("📋 Antwort kopieren:", value=email_text, height=150)

except Exception as e:
    st.error(f"Error reading Excel file: {e}")
