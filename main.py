from datetime import date
import mysql.connector
from mysql.connector import Error
from connect import connect_to_sql
from insert import (
    insert_user,
    insert_budget,
    insert_categories,
    insert_transactions,
    insert_bank_accounts
)

def main():
    conn = connect_to_sql()
    cursor = conn.cursor(dictionary=True)

    try:
        user_id = insert_user(cursor, 'Ben', 'Donohue', 'ben@example.com', '555-1234', '2000-01-01', 'hashed_pw')
        food_category_id = insert_categories(cursor, 'Food')
        account_id = insert_bank_accounts(cursor, user_id, 'Chase', 12345678, 1000.00, 'Checking')
        budget_id = insert_budget(cursor, user_id, food_category_id, 400.00, '2026-04-01', '2026-04-30')
        transaction_id = insert_transactions(cursor, account_id,food_category_id, 'Grocery', 50.00, '2026-04-03')

        conn.commit()

        cursor.execute("SELECT * FROM remaining_budget WHERE budget_id=%s", (budget_id,))
        print("Remaining budget:", cursor.fetchone())

        cursor.execute("SELECT current_balance FROM bank_accounts WHERE account_id=%s", (account_id,))
        print("Updated account balance:", cursor.fetchone()['current_balance'])

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

