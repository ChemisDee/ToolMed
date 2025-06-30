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

                email_text = f"""Vielen Dank für Ihre Anfrage,

Unsere Preise richten sich nach der Analysenliste des Bundesamts für Gesundheit (BAG), wobei 1 Taxpunkt (TP) einem Betrag von 1 CHF entspricht.
Die aktuelle Analysenliste finden Sie unter folgendem Link:
https://www.bag.admin.ch/bag/de/home/versicherungen/krankenversicherung/krankenversicherung-leistungen-tarife/Analysenliste.html

Bitte beachten Sie, dass die Kosten für Laboruntersuchungen nur bei ärztlicher Verordnung von der Krankenkasse übernommen werden.
Die voraussichtlichen Kosten Ihrer Untersuchungen habe ich Ihnen im Anhang/weiter unten kurz zusammengestellt (alle Angaben ohne Gewähr).

Für die Blutentnahme können Sie ohne Voranmeldung in unser Drop-In-Ambulatorium kommen. Unsere Öffnungszeiten sind:

Montag bis Freitag: 07:30 – 18:00 Uhr
Samstag: 07:30 – 11:30 Uhr

Ich hoffe, Ihnen mit diesen Informationen weitergeholfen zu haben und freue mich, Sie bald bei uns begrüssen zu dürfen.

Freundliche Grüsse,

*** ENGLISH VERSION ***
Thank you very much for your inquiry.

Our pricing is based on the Swiss Federal Office of Public Health's list of analyses, where 1 tax point (TP) corresponds to CHF 1.
You can find the current list here:
https://www.bag.admin.ch/bag/en/home/versicherungen/krankenversicherung/krankenversicherung-leistungen-tarife/Analysenliste.html

Please note that laboratory tests are only covered by health insurance with a valid medical prescription.
I have briefly outlined the estimated costs for your tests below/attached (all information without guarantee).

You are welcome to come to our drop-in ambulatory unit for the blood draw—no appointment is necessary. Our opening hours are:

Monday to Friday: 07:30 am – 6:00 pm
Saturday: 07:30 am – 11:30 am

I hope this information is helpful, and we look forward to welcoming you soon.

Kind regards,
[Your Name]

"""

                st.markdown("### ✉️ Vorschlag für Antwort-E-Mail")
                st.text_area("📋 Antwort kopieren:", value=email_text, height=150)

except Exception as e:
    st.error(f"Error reading Excel file: {e}")
