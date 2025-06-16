# 💊 Excel Price Summation Tool

A web app to calculate total prices based on medical test names or synonyms from an Excel sheet.

## 📂 Excel File Requirements
Your Excel file must contain **three columns**:
- `Name`
- `Synonym` (can be empty)
- `Price` (numeric)

## 🔍 Features
- Upload `.xlsx` or `.xls` file
- Fuzzy matching (case-insensitive, typo-tolerant)
- Enter names or synonyms (comma-separated)
- Outputs matched rows and total price

## 🚀 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🌍 Host Online
You can deploy this app for free via [Streamlit Cloud](https://streamlit.io/cloud).

1. Push `app.py`, `requirements.txt`, and `README.md` to a GitHub repo
2. Deploy via Streamlit Cloud using that repo
