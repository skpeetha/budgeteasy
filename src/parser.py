import fitz  # PyMuPDF
import pandas as pd
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_transactions_from_text(text):
    lines = [line.strip() for line in text.splitlines()]
    transactions = []
    i = 0
    prev_balance = None
    current_date = ""
    current_value_date = ""

    def is_date_line(line):
        return re.match(r"^\d{2} \w{3} \d{2}", line)

    def is_amount(val):
        return re.match(r"^\d[\d,]*\.\d{2}$", val.replace(",", ""))

    while i < len(lines):
        line = lines[i]

        # -- Start of a new dated transaction --
        if is_date_line(line):
            date_parts = line.split()
            current_date = " ".join(date_parts[0:3])
            current_value_date = " ".join(date_parts[3:6]) if len(date_parts) >= 6 else current_date
            i += 1
        elif line == "":
            i += 1
            continue  # Skip empty line
        else:
            # Start a new transaction (re-use date from previous line)
            pass

        desc_lines = []
        while i < len(lines) and not is_date_line(lines[i]) and not is_amount(lines[i]):
            if lines[i]:  # not empty
                desc_lines.append(lines[i])
            i += 1

        description = " ".join(desc_lines)

        # Get amounts
        numeric_values = []
        while i < len(lines) and (is_amount(lines[i]) or lines[i] == ""):
            if is_amount(lines[i]):
                numeric_values.append(lines[i].replace(",", ""))
            i += 1

        deposit = withdrawal = balance = None

        if len(numeric_values) == 1:
            balance = numeric_values[0]
        elif len(numeric_values) == 2:
            amount, balance = map(float, numeric_values)
            if prev_balance is not None:
                if balance > prev_balance:
                    deposit = amount
                else:
                    withdrawal = amount
            else:
                withdrawal = amount
        elif len(numeric_values) == 3:
            deposit, withdrawal, balance = numeric_values

        if balance is not None:
            prev_balance = float(balance)

        # Only append if meaningful content exists
        if description and (deposit or withdrawal):
            transactions.append({
                "date": current_date,
                "value_date": current_value_date,
                "description": description,
                "cheque": None,
                "deposit": deposit,
                "withdrawal": withdrawal,
                "balance": balance
            })

    return pd.DataFrame(transactions)
