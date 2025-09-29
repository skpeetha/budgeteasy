from src.parser import extract_transactions_from_text, extract_text_from_pdf
from src.categorize import categorize_transactions
from src.visualize import plot_expense_pie

text = extract_text_from_pdf("eStatement250525140352407953489.pdf")
df = extract_transactions_from_text(text)

df['category'] = df.apply(categorize_transactions, axis=1)
plot_expense_pie(df)
