# tests/test_parser.py

import pytest
import pandas as pd
from src.parser import extract_transactions_from_text

@pytest.fixture
def sample_text():
    return """
Description
Cheque
Deposit
Withdrawal
Balance
01 May 23 01 May 23 BALANCE FORWARD
42,508.51 
 
 
UPI/348633937939/
004001624108/HARISHSN111@OKICICI/
HARISH S N/ICIC0000040/UPI/
348633937939/ICICI BANK LTD/
 
1.00
 
42,509.51 
 
 
UPI/312051412025/
000205035327/CREDPAY@ICICI/
CREDDREAMPLUG/ICIC0DC0099/SECURITY
DEPOSIT PAYMENT
312051412025/
 
30,000.00
 
72,509.51
03 May 23 03 May 23 LAZYPAY PRIVATE LIMITED/LAZYPAYPVTLTD.RZP@ICICI/
LAZYPAY LOAN PAYMENT


372.00
40,036.51
"""

def test_transaction_count(sample_text):
    df = extract_transactions_from_text(sample_text)
    # Expecting 3 actual transactions, excluding the BALANCE FORWARD
    assert len(df) == 3

def test_column_presence(sample_text):
    df = extract_transactions_from_text(sample_text)
    expected_columns = {'date', 'value_date', 'description', 'cheque', 'deposit', 'withdrawal', 'balance'}
    assert expected_columns.issubset(set(df.columns))

def test_multi_line_description(sample_text):
    df = extract_transactions_from_text(sample_text)
    desc = df.iloc[1]["description"]
    assert "CREDPAY@ICICI" in desc
    assert "SECURITY" in desc  # description spans multiple lines

def test_balance_parsing(sample_text):
    df = extract_transactions_from_text(sample_text)
    print(df)
    assert df.iloc[0]["deposit"] == 1.0
    assert df.iloc[0]["balance"] == 42509.51
