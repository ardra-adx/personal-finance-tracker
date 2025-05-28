import sqlite3
import pandas as pd
from tabulate import tabulate
from datetime import datetime

DB_NAME = "finance_tracker.db"

def setup_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                description TEXT,
                amount REAL,
                category TEXT
            )
        ''')
        conn.commit()

def categorize(description):
    description = description.lower()
    if "salary" in description:
        return "Income"
    elif any(word in description for word in ["coffee", "restaurant", "food"]):
        return "Food"
    elif any(word in description for word in ["rent", "emi", "loan"]):
        return "Housing"
    else:
        return "Other"

def import_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # Categorize transactions safely with .loc to avoid warning
        df.loc[:, 'category'] = df['Description'].apply(categorize)
        
        # Insert data into SQLite database
        conn = sqlite3.connect(DB_NAME)
        df.to_sql('transactions', conn, if_exists='append', index=False)
        conn.close()
        
        print("Imported successfully.")
    except Exception as e:
        print(f"Error importing CSV: {e}")


def monthly_report(month, year):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT date, description, amount, category FROM transactions
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
        ''', (month.zfill(2), year))
        rows = c.fetchall()

        if not rows:
            print("No transactions found.")
            return

        df = pd.DataFrame(rows, columns=["Date", "Description", "Amount", "Category"])
        print("\nAll Transactions:\n")
        print(tabulate(df, headers="keys", tablefmt="grid"))

        print("\nSummary:\n")
        summary = df.groupby("Category")["Amount"].sum().reset_index()
        print(tabulate(summary, headers="keys", tablefmt="grid"))

def main():
    setup_db()
    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Import Transactions from CSV")
        print("2. Generate Monthly Report")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            path = input("Enter CSV file path (like transactions.csv): ")
            try:
                import_csv(path)
            except Exception as e:
                print("Error:", e)

        elif choice == '2':
            month = input("Enter month (e.g. 05): ")
            year = input("Enter year (e.g. 2024): ")
            monthly_report(month, year)

        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()