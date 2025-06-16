import pandas as pd
from rapidfuzz import fuzz

def normalize(text):
    return str(text).strip().lower() if pd.notna(text) else ""

def fuzzy_match(needle, haystack_list, threshold=85):
    return any(fuzz.ratio(needle, item) >= threshold for item in haystack_list)

def get_fuzzy_matches(df, input_text):
    df = df.copy()
    df["Name_norm"] = df["Name"].apply(normalize)

    # Split comma-separated synonyms into a list of normalized entries
    df["Synonyms_norm"] = df["Synonym"].apply(lambda x: [normalize(s) for s in str(x).split(",")] if pd.notna(x) else [])

    entries = [normalize(e) for e in input_text.split(",") if e.strip()]
    matched_rows = []

    for _, row in df.iterrows():
        haystack = [row["Name_norm"]] + row["Synonyms_norm"]
        if any(fuzzy_match(entry, haystack) for entry in entries):
            matched_rows.append(row)

    return pd.DataFrame(matched_rows)
