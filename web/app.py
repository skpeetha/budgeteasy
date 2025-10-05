# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import traceback
import tempfile
from werkzeug.utils import secure_filename

from src.parser import extract_transactions_from_text, extract_text_from_pdf, calculate_file_hash
from src.categorize import categorize_transactions
from src.visualize import plot_expense_pie
from src.db import init_db, insert_statement, insert_transactions, get_statement_by_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Max 10MB

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file uploaded")
            return redirect(url_for('index'))

        file = request.files["file"]
        if file.filename == "":
            flash("No file selected")
            return redirect(url_for('index'))

        # Save uploaded file temporarily
        if file.filename and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
        else:
            flash("Invalid file type. Please upload a PDF.")
            return redirect(url_for('index'))

        # Calculate hash
        filehash = calculate_file_hash(filepath)

        # Check if already processed
        existing = get_statement_by_hash(filehash)
        if existing:
            flash("This statement was already uploaded. Skipping.")
            #return redirect(url_for("index"))

        # Parse transactions
        try:            
            text = extract_text_from_pdf(filepath)
            df = extract_transactions_from_text(text)
            
            if not isinstance(df, pd.DataFrame):
                flash("Error: Could not parse transactions from PDF.")
                return redirect(url_for('index'))

            if df.empty:
                flash("No transactions found in statement.")
                return redirect(url_for('index'))

            # Categorize
            df['category'] = df.apply(categorize_transactions, axis=1)
            df = df.astype(object).where(pd.notnull(df), None)

            # Save to DB (after parsing is successful)
            statement_id = insert_statement(
                filename=file.filename,
                filehash=filehash,
                bank_name="Unknown Bank",  # could be detected later
                statement_type="normal"
            )
            insert_transactions(statement_id, df)

            # Plot and save chart
            static_dir = os.path.join(os.path.dirname(__file__), 'static')
            plot_path = os.path.join(static_dir, "category_pie.png")
            plot_expense_pie(df, output_path=plot_path)

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
            flash(f"Error processing file:\n{traceback.format_exc()}")
            print(traceback.format_exc())
            return redirect(url_for('index'))

    return render_template("index.html")

if __name__ == "__main__":
    init_db()  # ensure DB schema exists at startup
    app.run(debug=True)
