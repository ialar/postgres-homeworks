"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import os
from pathlib import Path

import psycopg2

employees_data_path = str(Path(__file__).resolve().parent / 'north_data' / 'employees_data.csv')
customers_data_path = str(Path(__file__).resolve().parent / 'north_data' / 'customers_data.csv')
orders_data_path = str(Path(__file__).resolve().parent / 'north_data' / 'orders_data.csv')

conn = psycopg2.connect(database='north', user='postgres', password=os.getenv("PSQL_PASS"))


def main():
    fill_employees_data(path=employees_data_path)
    fill_customers_data(path=customers_data_path)
    fill_orders_data(path=orders_data_path)


def fill_employees_data(path):
    with open(path) as file:
        reader = csv.reader(file)
        next(reader)
        with conn.cursor() as cur:
            cur.executemany('INSERT INTO employees '
                            '(employee_id, first_name, last_name, title, birth_date, notes) '
                            'VALUES (%s, %s, %s, %s, %s, %s)', reader)
        conn.commit()


def fill_customers_data(path):
    with open(path) as file:
        reader = csv.reader(file)
        next(reader)
        with conn.cursor() as cur:
            cur.executemany('INSERT INTO customers '
                            '(customer_id, company_name, contact_name) '
                            'VALUES (%s, %s, %s)', reader)
        conn.commit()


def fill_orders_data(path):
    with open(path) as file:
        reader = csv.reader(file)
        next(reader)
        with conn.cursor() as cur:
            cur.executemany('INSERT INTO orders '
                            '(order_id, customer_id, employee_id, order_date, ship_city) '
                            'VALUES (%s, %s, %s, %s, %s)', reader)
        conn.commit()


if __name__ == "__main__":
    try:
        main()
    finally:
        conn.close()
