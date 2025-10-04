# src/db.py
import sqlite3
import os

DB_NAME = "budgeteasy.db"


def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # enables dict-like row access
    return conn


def init_db():
    """Initialize database with tables if they don’t exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS statements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        filehash TEXT NOT NULL,
        bank_name TEXT,
        statement_type TEXT CHECK(statement_type IN ('normal', 'credit')),
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        statement_id INTEGER,
        date TEXT,
        value_date TEXT,
        description TEXT,
        cheque TEXT,
        deposit REAL,
        withdrawal REAL,
        balance REAL,
        category TEXT,
        FOREIGN KEY(statement_id) REFERENCES statements(id)
    );
    """)

    conn.commit()
    conn.close()


def insert_statement(filename, filehash, bank_name, statement_type):
    """Insert a new statement into the statements table and return its id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO statements (filename, filehash, bank_name, statement_type) VALUES (?, ?, ?, ?)",
        (filename, filehash, bank_name, statement_type)
    )
    conn.commit()
    statement_id = cursor.lastrowid
    conn.close()
    return statement_id


def get_statement_by_hash(filehash):
    """Check if a statement with this hash already exists."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM statements WHERE filehash = ?", (filehash,))
    result = cursor.fetchone()
    conn.close()
    return result


def insert_transactions(statement_id, df):
    """Insert parsed transactions linked to a statement."""
    conn = get_db_connection()
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO transactions 
            (statement_id, date, value_date, description, cheque, deposit, withdrawal, balance, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                statement_id,
                row.get("date"),
                row.get("value_date"),
                row.get("description"),
                row.get("cheque"),
                row.get("deposit"),
                row.get("withdrawal"),
                row.get("balance"),
                row.get("category")
            )
        )
    conn.commit()
    conn.close()
