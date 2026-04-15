import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]   # backend/
DB_PATH = BASE_DIR / "data" / "retail.db"
CSV_PATH = BASE_DIR / "data" / "retail_sales.csv"

def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found at: {CSV_PATH}")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    print("Creating DB at:", DB_PATH)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # Drop table if exists (clean rebuild)
    cur.execute("DROP TABLE IF EXISTS sales")

    # Create table
    cur.execute("""
    CREATE TABLE sales (
        order_id TEXT,
        order_date TEXT,
        store_id TEXT,
        region TEXT,
        product_id TEXT,
        category TEXT,
        quantity INTEGER,
        unit_price REAL,
        discount REAL
    )
    """)

    # Insert CSV data
    with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        rows = []
        for r in reader:
            rows.append((
                r["order_id"],
                r["order_date"],
                r["store_id"],
                r["region"],
                r["product_id"],
                r["category"],
                int(r["quantity"]),
                float(r["unit_price"]),
                float(r["discount"])
            ))

    cur.executemany(
        "INSERT INTO sales VALUES (?,?,?,?,?,?,?,?,?)",
        rows
    )

    con.commit()
    con.close()

    print(f"✅ Imported {len(rows)} rows into retail.db")

if __name__ == "__main__":
    main()