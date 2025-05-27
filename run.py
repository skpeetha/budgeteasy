from parser import extract_text_from_pdf, extract_transactions_from_text, categorize_transaction

text = extract_text_from_pdf("eStatement250525140352407953489.pdf")

df = extract_transactions_from_text(text)
df['category'] = df.apply(categorize_transaction, axis=1)
print([category for category in df['category'].unique()])

df.to_csv("output.csv", index=False)