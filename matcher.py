import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Price Summation", layout="centered")
st.title("📊 Excel Price Summation Tool")

DEFAULT_FILE = "DefaultPreise.xlsx"

# Dateiupload oder Fallback
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])
use_default = False

try:
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.success("Custom file loaded.")
    else:
        df = pd.read_excel(DEFAULT_FILE)
        st.info("Using built-in price list.")
        use_default = True

    # Spaltenprüfung
    if not {'Name', 'Synonym', 'Price'}.issubset(df.columns):
        st.error("Excel must contain 'Name', 'Synonym', and 'Price' columns.")
    else:
        input_text = st.text_input("Enter names or synonyms (comma-separated):")

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
                st.success(f"💰 Total Price after removal: {total:.2f} CHF")

                # Unmatched-Eingaben anzeigen
                entries = [entry.strip().lower() for entry in input_text.split(",") if entry.strip()]
                matched_terms = set()
                for _, row in matched_df.iterrows():
                    matched_terms.add(row["Name"].strip().lower())
                    matched_terms.update([s.strip().lower() for s in str(row["Synonym"]).split(",")])
                unmatched = [e for e in entries if not any(e in matched for matched in matched_terms)]
                if unmatched:
                    st.markdown("### ⚠️ Nicht gefundene Eingaben")
                    st.warning(f"Die folgenden Begriffe konnten nicht zugeordnet werden: {', '.join(unmatched)}")

                # Vorschlag für Antwort-E-Mail
                email_text = f"""Guten Tag,

Vielen Dank für Ihre Anfrage. Die Kosten für die von Ihnen gewünschten Analysen belaufen sich total auf {total:.2f} CHF (Angaben ohne Gewähr).

Freundliche Grüsse,
"""
                st.markdown("### ✉️ Vorschlag für Antwort-E-Mail")
                st.text_area("📋 Antwort kopieren:", value=email_text, height=150)

except Exception as e:
    st.error(f"Fehler beim Einlesen der Excel-Datei: {e}")

