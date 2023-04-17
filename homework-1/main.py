"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import csv
from datetime import date

customers = "customers_data.csv"
employees = "employees_data.csv"
orders = "orders_data.csv"

conn = psycopg2.connect(
    host='localhost',
    database='north',
    user='postgres',
    password='12345'
)
try:
    with conn:
        with conn.cursor() as cur:
            with open(f"north_data/{customers}", "r", encoding="utf-8") as file:
                rows = csv.reader(file)
                for row in rows:
                    cur.execute("INSERT INTO customers VALUES (%s, %s, %s)", tuple(row))

            with open(f"north_data/{employees}", "r", encoding="utf-8") as file:
                rows = csv.DictReader(file)
                for row in rows:
                    first_name = row["first_name"]
                    last_name = row["last_name"]
                    title = row["title"]
                    year, month, day = row["birth_date"].split("-")
                    birth_date = date(int(year), int(month), int(day))
                    notes = row["notes"]
                    cur.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, title, birth_date, notes))

            with open(f"north_data/{orders}", "r", encoding="utf-8") as file:
                rows = csv.DictReader(file)
                for row in rows:
                    order_id = row["order_id"]
                    customer_id = row["customer_id"]
                    employee_id = row["employee_id"]
                    year, month, day = row["order_date"].split("-")
                    order_date = date(int(year), int(month), int(day))
                    ship_city = row["ship_city"]
                    cur.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s)", (order_id, customer_id, employee_id, order_date, ship_city))
finally:
    conn.close()