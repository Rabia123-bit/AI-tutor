import sqlite3
from pathlib import Path
from typing import Any, Dict, List

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "retail.db"


def _connect():
    return sqlite3.connect(DB_PATH)


def _fetch_all_dicts(cursor) -> List[Dict[str, Any]]:
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# -----------------------------
# KPI analyses
# -----------------------------
def total_revenue() -> Dict[str, Any]:
    sql = """
    SELECT ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS total_revenue
    FROM sales
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    con.close()

    return {
        "analysis_type": "kpi",
        "metric": "total_revenue",
        "value": row[0] or 0.0
    }


def total_orders() -> Dict[str, Any]:
    sql = "SELECT COUNT(DISTINCT order_id) AS total_orders FROM sales"
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    con.close()

    return {
        "analysis_type": "kpi",
        "metric": "total_orders",
        "value": row[0] or 0
    }


def average_order_value() -> Dict[str, Any]:
    sql = """
    SELECT ROUND(
        SUM(quantity * unit_price * (1 - discount)) / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS average_order_value
    FROM sales
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    con.close()

    return {
        "analysis_type": "kpi",
        "metric": "average_order_value",
        "value": row[0] or 0.0
    }


def top_categories() -> Dict[str, Any]:
    sql = """
    SELECT category,
           ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue
    FROM sales
    GROUP BY category
    ORDER BY revenue DESC
    LIMIT 5
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    rows = _fetch_all_dicts(cur)
    con.close()

    return {
        "analysis_type": "kpi",
        "metric": "top_categories",
        "rows": rows
    }


# -----------------------------
# SQL analyses
# -----------------------------
def sql_sales_by_category() -> Dict[str, Any]:
    sql = """
    SELECT category,
           ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue
    FROM sales
    GROUP BY category
    ORDER BY revenue DESC
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    rows = _fetch_all_dicts(cur)
    con.close()

    return {
        "analysis_type": "sql",
        "analysis_name": "sales_by_category",
        "sql_query": sql.strip(),
        "rows": rows
    }


def sql_top_stores() -> Dict[str, Any]:
    sql = """
    SELECT store_id,
           region,
           ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue
    FROM sales
    GROUP BY store_id, region
    ORDER BY revenue DESC
    LIMIT 10
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    rows = _fetch_all_dicts(cur)
    con.close()

    return {
        "analysis_type": "sql",
        "analysis_name": "top_stores",
        "sql_query": sql.strip(),
        "rows": rows
    }


def sql_daily_revenue() -> Dict[str, Any]:
    sql = """
    SELECT order_date,
           ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue
    FROM sales
    GROUP BY order_date
    ORDER BY order_date ASC
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    rows = _fetch_all_dicts(cur)
    con.close()

    return {
        "analysis_type": "sql",
        "analysis_name": "daily_revenue",
        "sql_query": sql.strip(),
        "rows": rows
    }


# -----------------------------
# Dashboard analyses
# -----------------------------
def dashboard_sales_overview() -> Dict[str, Any]:
    con = _connect()
    cur = con.cursor()

    cur.execute("""
        SELECT ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS total_revenue,
               COUNT(DISTINCT order_id) AS total_orders,
               ROUND(SUM(quantity * unit_price * (1 - discount)) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS aov
        FROM sales
    """)
    kpi_row = cur.fetchone()

    cur.execute("""
        SELECT order_date,
               ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue
        FROM sales
        GROUP BY order_date
        ORDER BY order_date ASC
    """)
    trend_rows = _fetch_all_dicts(cur)

    con.close()

    return {
        "analysis_type": "dashboard",
        "analysis_name": "sales_overview",
        "kpis": {
            "total_revenue": kpi_row[0] or 0.0,
            "total_orders": kpi_row[1] or 0,
            "average_order_value": kpi_row[2] or 0.0,
        },
        "trend": trend_rows
    }


def dashboard_store_comparison() -> Dict[str, Any]:
    sql = """
    SELECT store_id,
           region,
           ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue
    FROM sales
    GROUP BY store_id, region
    ORDER BY revenue DESC
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    rows = _fetch_all_dicts(cur)
    con.close()

    return {
        "analysis_type": "dashboard",
        "analysis_name": "store_comparison",
        "rows": rows
    }


def dashboard_category_performance() -> Dict[str, Any]:
    sql = """
    SELECT category,
           ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue,
           SUM(quantity) AS units_sold
    FROM sales
    GROUP BY category
    ORDER BY revenue DESC
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    rows = _fetch_all_dicts(cur)
    con.close()

    return {
        "analysis_type": "dashboard",
        "analysis_name": "category_performance",
        "rows": rows
    }


# -----------------------------
# ETL analyses
# -----------------------------
def data_quality_summary() -> Dict[str, Any]:
    sql = """
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT order_id) AS distinct_orders,
        COUNT(DISTINCT store_id) AS distinct_stores,
        COUNT(DISTINCT product_id) AS distinct_products,
        MIN(order_date) AS start_date,
        MAX(order_date) AS end_date,
        SUM(CASE WHEN order_id IS NULL OR order_id = '' THEN 1 ELSE 0 END) AS missing_order_id,
        SUM(CASE WHEN order_date IS NULL OR order_date = '' THEN 1 ELSE 0 END) AS missing_order_date,
        SUM(CASE WHEN store_id IS NULL OR store_id = '' THEN 1 ELSE 0 END) AS missing_store_id,
        SUM(CASE WHEN product_id IS NULL OR product_id = '' THEN 1 ELSE 0 END) AS missing_product_id
    FROM sales
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    con.close()

    return {
        "analysis_type": "etl",
        "analysis_name": "data_quality_summary",
        "summary": {
            "total_rows": row[0],
            "distinct_orders": row[1],
            "distinct_stores": row[2],
            "distinct_products": row[3],
            "start_date": row[4],
            "end_date": row[5],
            "missing_order_id": row[6],
            "missing_order_date": row[7],
            "missing_store_id": row[8],
            "missing_product_id": row[9],
        }
    }


def etl_category_standardization_check() -> Dict[str, Any]:
    sql = """
    SELECT category, COUNT(*) AS row_count
    FROM sales
    GROUP BY category
    ORDER BY row_count DESC
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    rows = _fetch_all_dicts(cur)
    con.close()

    return {
        "analysis_type": "etl",
        "analysis_name": "category_standardization_check",
        "rows": rows
    }


# -----------------------------
# Data Warehousing analyses
# -----------------------------
def warehouse_dimension_summary() -> Dict[str, Any]:
    con = _connect()
    cur = con.cursor()

    cur.execute("SELECT COUNT(DISTINCT store_id) FROM sales")
    store_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT region) FROM sales")
    region_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT product_id) FROM sales")
    product_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT category) FROM sales")
    category_count = cur.fetchone()[0]

    cur.execute("SELECT MIN(order_date), MAX(order_date) FROM sales")
    date_range = cur.fetchone()

    con.close()

    return {
        "analysis_type": "data_warehousing",
        "analysis_name": "dimension_summary",
        "dimensions": {
            "stores": store_count,
            "regions": region_count,
            "products": product_count,
            "categories": category_count,
            "start_date": date_range[0],
            "end_date": date_range[1],
        }
    }


def fact_table_summary() -> Dict[str, Any]:
    sql = """
    SELECT COUNT(*) AS fact_rows,
           ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS total_revenue,
           SUM(quantity) AS total_units
    FROM sales
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    con.close()

    return {
        "analysis_type": "data_warehousing",
        "analysis_name": "fact_table_summary",
        "fact_summary": {
            "fact_rows": row[0],
            "total_revenue": row[1],
            "total_units": row[2],
        }
    }


# -----------------------------
# Predictive Analytics analyses
# -----------------------------
def daily_revenue_trend() -> Dict[str, Any]:
    sql = """
    SELECT order_date,
           ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue
    FROM sales
    GROUP BY order_date
    ORDER BY order_date ASC
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(sql)
    rows = _fetch_all_dicts(cur)
    con.close()

    return {
        "analysis_type": "predictive_analytics",
        "analysis_name": "daily_revenue_trend",
        "rows": rows
    }


def forecast_readiness_summary() -> Dict[str, Any]:
    con = _connect()
    cur = con.cursor()

    cur.execute("""
        SELECT COUNT(*) AS total_rows,
               COUNT(DISTINCT order_date) AS distinct_days,
               COUNT(DISTINCT product_id) AS distinct_products,
               COUNT(DISTINCT store_id) AS distinct_stores
        FROM sales
    """)
    row = cur.fetchone()

    con.close()

    return {
        "analysis_type": "predictive_analytics",
        "analysis_name": "forecast_readiness_summary",
        "summary": {
            "total_rows": row[0],
            "distinct_days": row[1],
            "distinct_products": row[2],
            "distinct_stores": row[3],
        }
    }