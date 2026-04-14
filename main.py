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
from delete import (
    delete_user,
    delete_budget,
    delete_category,
    delete_transaction,
    delete_bank_account
)
from update import (
    update_user,
    update_budget,
    update_category,
    update_transaction,
    update_bank_account
)

def main():
    conn = connect_to_sql()
    cursor = conn.cursor(dictionary=True)

    try:
        categories = [
            "Food",
            "Rent",
            "Utilities",
            "Transportation",
            "Entertainment",
            "Healthcare",
            "Insurance",
            "Shopping",
            "Education",
            "Travel",
            "Savings",
            "Miscellaneous"
        ]

        category_ids = {}

        for cat in categories:
            cid = insert_categories(cursor, cat)
            category_ids[cat] = cid

        conn.commit()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

