from datetime import date
import mysql.connector

def insert_user(cursor, first_name, last_name, email_address, phone_number, date_of_birth, password):
    query = """
    INSERT INTO user (first_name, last_name, email_address, phone_number, date_of_birth, password)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    if isinstance(date_of_birth, str):
        year, month, day = map(int, date_of_birth.split('-'))
        date_of_birth = date(year, month, day)

    cursor.execute(query, (first_name, last_name, email_address, phone_number, date_of_birth, password))
    return cursor.lastrowid

def insert_bank_accounts(cursor, user_id, bank_name, account_number, current_balance, account_type):
    query = """
    INSERT INTO bank_accounts (user_id, bank_name, account_number, current_balance, account_type)
    VALUES (%s, %s, %s, %s, %s)
    """

    account_number = int(account_number)
    current_balance = float(current_balance)

    cursor.execute(query, (user_id, bank_name, account_number, current_balance, account_type))
    return cursor.lastrowid

def insert_budget(cursor, user_id, category_id, target_amount, start_date, end_date):
    query = """
    INSERT INTO budget (user_id, category_id, target_amount, start_date, end_date)
    VALUES (%s, %s, %s, %s, %s)
    """

    target_amount = float(target_amount)
    if isinstance(start_date, str):
        year, month, day = map(int, start_date.split('-'))
        start_date = date(year, month, day)
    if isinstance(end_date, str):
        year, month, day = map(int, end_date.split('-'))
        end_date = date(year, month, day)

    cursor.execute(query, (user_id, category_id, target_amount, start_date, end_date))
    return cursor.lastrowid

def insert_categories(cursor, category_name):
    query = """
    INSERT INTO categories (category_name)
    VALUES (%s)
    """

    cursor.execute(query, (category_name,))
    return cursor.lastrowid

def insert_transactions(cursor, account_id, category_id, transaction_name, transaction_amount, transaction_date):
    query = """
    INSERT INTO transactions (account_id, category_id, transaction_name, transaction_amount, transaction_date)
    VALUES (%s, %s, %s, %s, %s)
    """

    transaction_amount = float(transaction_amount)
    if isinstance(transaction_date, str):
        year, month, day = map(int, transaction_date.split('-'))
        transaction_date = date(year, month, day)

    cursor.execute(query, (account_id, category_id, transaction_name, transaction_amount, transaction_date))
    return cursor.lastrowid






