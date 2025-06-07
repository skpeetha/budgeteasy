# 🧾 budgeteasy

**budgeteasy** is a simple, privacy-focused tool that helps you parse bank statements (PDFs), extract and categorize transactions, and visualize spending — all on your local machine.

---

## 🔧 Features

- ✅ Extract transactions from bank statement PDFs (using `PyMuPDF`)
- ✅ Handle multi-line, multi-format statement entries
- ✅ Automatically categorize expenses (e.g. Food, Rent, Utilities)
- ✅ Export data as `.csv`
- ✅ Visualize category-wise spending via pie charts
- ✅ Minimal web interface using Flask
- ✅ Unit tests for parsing and categorization

---

## 📁 Project Structure

```
budgeteasy/
├── app.py                  # Flask web app entry point
├── run.py                  # CLI entry to run extract + categorize + plot
├── main.py                 # Alternative manual flow for testing
├── src/
│   ├── parser.py           # PDF parsing and transaction extraction
│   ├── categorize.py       # Transaction categorization logic
│   ├── visualize.py        # Generates pie chart using matplotlib
│   └── utils.py            # (optional) Helper functions
├── tests/
│   └── test_parser.py      # Pytest-based tests for parser functions
├── web/
│   ├── templates/
│   │   └── index.html      # Upload form and result display
│   └── static/
│       └── category_pie.png  # Output chart (generated at runtime)
└── README.md
```

---

## ▶️ Usage

### 🔹 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔹 2. Launch Web UI

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser to:
- Upload a PDF statement
- View the extracted transaction table
- See categorized spending
- View a pie chart of expenses

*All processing is done offline—no data is sent externally.*

### 🔹 3. Run from CLI

```bash
python run.py <path-to-pdf>
```

This parses the PDF, categorizes transactions, and saves a pie chart as `output/category_pie.png`.

---

## 📊 Sample Output

*(For illustration; actual output depends on your data)*

---

## 🧪 Testing

Run the tests with:

```bash
pytest
```

Includes:
- Parsing logic validation
- Multi-line and edge-case handling
- Categorization accuracy

---

## 🛡️ Privacy

All PDF parsing, categorization, and visualization happen **locally**, with no external API calls—your financial data remains secure.

---

## 🚧 Future Enhancements

- OCR for scanned statements
- Bar/line charts and time-series views
- Monthly/quarterly summaries
- Downloadable CSV from the web UI
- Search/filter capabilities in UI

---

## 🤝 Contributions

Feel free to suggest improvements or submit pull requests!

[GitHub Repository](https://github.com/skpeetha/budgeteasy)