# app.py
import os
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd

from src.parser import extract_transactions_from_text
from src.categorize import categorize_transactions
from src.visualize import plot_expense_pie
from src.db import init_db, insert_statement, insert_transactions, get_statement_by_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def calculate_file_hash(filepath):
    """Generate SHA256 hash for a given file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file uploaded")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        # Save uploaded file temporarily
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Calculate hash
        filehash = calculate_file_hash(filepath)

        # Check if already processed
        existing = get_statement_by_hash(filehash)
        if existing:
            flash("This statement was already uploaded. Skipping.")
            return redirect(url_for("index"))

        # Parse transactions
        try:
            import fitz  # pyMuPDF
            doc = fitz.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text()

            df = extract_transactions_from_text(text)

            if df.empty:
                flash("No transactions found in statement.")
                return redirect(request.url)

            # Categorize
            df = categorize_transactions(df)

            # Save to DB (after parsing is successful)
            statement_id = insert_statement(
                filename=file.filename,
                filehash=filehash,
                bank_name="Unknown Bank",  # could be detected later
                statement_type="normal"
            )
            insert_transactions(statement_id, df)

            # Plot and save chart
            plot_path = os.path.join("static", "category_pie.png")
            plot_expense_pie(df, save_path=plot_path)

            # Summary stats
            total_spent = df["withdrawal"].sum(skipna=True)
            total_received = df["deposit"].sum(skipna=True)
            top_categories = (
                df.groupby("category")["withdrawal"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
            )

            return render_template(
                "index.html",
                tables=[df.to_html(classes="data", header="true", index=False)],
                plot_url=plot_path,
                total_spent=total_spent,
                total_received=total_received,
                top_categories=top_categories.to_dict()
            )

        except Exception as e:
            flash(f"Error processing file: {str(e)}")
            return redirect(request.url)

    return render_template("index.html")


if __name__ == "__main__":
    init_db()  # ensure DB schema exists at startup
    app.run(debug=True)
