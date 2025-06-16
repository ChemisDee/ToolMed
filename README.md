# 💊 Excel Price Summation Tool (with Fuzzy Matching and Row Removal)

This Streamlit web app allows you to calculate total prices from an Excel file containing medical test entries.

## 📂 Excel File Requirements
Your Excel file must contain these columns:
- `Name`
- `Synonym` (optional but recommended)
- `Price` (numeric)

## 🔍 Features
- Fuzzy matching on both `Name` and `Synonym`
- Case-insensitive and typo-tolerant
- Select and remove false positives before final price calculation

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🌍 Host Online
Deploy on [Streamlit Cloud](https://streamlit.io/cloud):

1. Push `app.py`, `matcher.py`, `requirements.txt`, and `README.md` to a GitHub repo
2. Deploy via Streamlit Cloud using that repo
