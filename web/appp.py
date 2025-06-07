import sys
sys.path.insert(0, '../')

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF
from src.parser import extract_transactions_from_text, extract_text_from_pdf
from src.categorize import categorize_transactions
from src.visualize import plot_expense_pie
import tempfile
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Max 10MB

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['statement']
        if uploaded_file and uploaded_file.filename.endswith('.pdf'):
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)

            text = extract_text_from_pdf(file_path)

            df = extract_transactions_from_text(text)
            df['category'] = df.apply(categorize_transactions, axis=1)

            static_dir = os.path.join(os.path.dirname(__file__), 'static')
            pie_path = os.path.join(static_dir, 'category_pie.png')

            plot_expense_pie(df, output_path=pie_path)

            return render_template('index.html', tables=[df.to_html(classes='table table-striped', index=False)],
                                   pie_chart=url_for('static', filename='category_pie.png'))
        else:
            return "Please upload a valid PDF file."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
