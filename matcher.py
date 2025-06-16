import pandas as pd
from rapidfuzz import fuzz

def normalize(text):
    return str(text).strip().lower() if pd.notna(text) else ""

def is_match(entry, haystack, threshold=92):
    entry_norm = normalize(entry)

    for item in haystack:
        item_norm = normalize(item)
        if entry_norm == item_norm:
            return True  # exact match
        if entry_norm in item_norm or item_norm in entry_norm:
            return True  # substring match
        if fuzz.ratio(entry_norm, item_norm) >= threshold:
            return True  # fuzzy match
    return False

def get_fuzzy_matches(df, input_text):
    df = df.copy()
    df["Name_norm"] = df["Name"].apply(normalize)
    df["Synonyms_norm"] = df["Synonym"].apply(
        lambda x: [normalize(s) for s in str(x).split(",")] if pd.notna(x) else []
    )

    entries = [normalize(e) for e in input_text.split(",") if e.strip()]
    matched_rows = []

    for _, row in df.iterrows():
        haystack = [row["Name_norm"]] + row["Synonyms_norm"]
        if any(is_match(entry, haystack) for entry in entries):
            matched_rows.append(row)

    return pd.DataFrame(matched_rows)
