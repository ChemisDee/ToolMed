import pandas as pd
from rapidfuzz import fuzz

def normalize(text):
    return str(text).strip().lower() if pd.notna(text) else ""

def tokenize_synonyms(syn_string):
    if pd.isna(syn_string):
        return []
    return [normalize(token) for token in str(syn_string).split(",")]

def is_precise_match(entry, candidates, threshold=95):
    for candidate in candidates:
        if entry == candidate:
            return True  # exakte Übereinstimmung
        if entry in candidate.split():  # ganzes Wort enthalten
            return True
        if (
            fuzz.ratio(entry, candidate) >= threshold and
            abs(len(entry) - len(candidate)) <= 1
        ):
            return True  # nur sehr ähnliche, fast gleich lange Treffer
    return False

def get_fuzzy_matches(df, input_text):
    df = df.copy()
    df["Name_norm"] = df["Name"].apply(normalize)
    df["Synonyms_norm"] = df["Synonym"].apply(tokenize_synonyms)

    entries = [normalize(e) for e in input_text.split(",") if e.strip()]
    matched_rows = []

    for _, row in df.iterrows():
        haystack = [row["Name_norm"]] + row["Synonyms_norm"]
        if any(is_precise_match(entry, haystack) for entry in entries):
            matched_rows.append(row)

    return pd.DataFrame(matched_rows)
