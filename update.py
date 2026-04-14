from datetime import date

def update_user(cursor, user_id, first_name=None, last_name=None, email_address=None, phone_number=None, date_of_birth=None, password=None):
    updates = []
    values = []

    if first_name is not None:
        updates.append("first_name=%s")
        values.append(first_name)
    if last_name is not None:
        updates.append("last_name=%s")
        values.append(last_name)
    if email_address is not None:
        updates.append("email_address=%s")
        values.append(email_address)
    if phone_number is not None:
        updates.append("phone_number=%s")
        values.append(phone_number)
    if date_of_birth is not None:
        if isinstance(date_of_birth, str):
            year, month, day = map(int, date_of_birth.split('-'))
            date_of_birth = date(year, month, day)
        updates.append("date_of_birth=%s")
        values.append(date_of_birth)
    if password is not None:
        updates.append("password=%s")
        values.append(password)
    if not updates:
        return 0

    values.append(user_id)
    query = f"UPDATE user SET {', '.join(updates)} WHERE user_id=%s"
    cursor.execute(query, tuple(values))
    return cursor.rowcount

def update_bank_account(cursor, account_id, bank_name=None, account_number=None, current_balance=None, account_type=None):
    updates = []
    values = []

    if bank_name is not None:
        updates.append("bank_name=%s")
        values.append(bank_name)
    if account_number is not None:
        updates.append("account_number=%s")
        values.append(int(account_number))
    if current_balance is not None:
        updates.append("current_balance=%s")
        values.append(float(current_balance))
    if account_type is not None:
        updates.append("account_type=%s")
        values.append(account_type)
    if not updates:
        return 0

    values.append(account_id)
    query = f"UPDATE bank_accounts SET {', '.join(updates)} WHERE account_id=%s"
    cursor.execute(query, tuple(values))
    return cursor.rowcount

def update_budget(cursor, budget_id, target_amount=None, start_date=None, end_date=None):
    updates = []
    values = []

    if target_amount is not None:
        updates.append("target_amount=%s")
        values.append(float(target_amount))
    if start_date is not None:
        if isinstance(start_date, str):
            year, month, day = map(int, start_date.split('-'))
            start_date = date(year, month, day)
        updates.append("start_date=%s")
        values.append(start_date)
    if end_date is not None:
        if isinstance(end_date, str):
            year, month, day = map(int, end_date.split('-'))
            end_date = date(year, month, day)
        updates.append("end_date=%s")
        values.append(end_date)

    if not updates:
        return 0

    values.append(budget_id)
    query = f"UPDATE budget SET {', '.join(updates)} WHERE budget_id=%s"
    cursor.execute(query, tuple(values))
    return cursor.rowcount

def update_transaction(cursor, transaction_id, transaction_name=None, transaction_amount=None, transaction_date=None, category_id=None):
    updates = []
    values = []

    if transaction_name is not None:
        updates.append("transaction_name=%s")
        values.append(transaction_name)
    if transaction_amount is not None:
        updates.append("transaction_amount=%s")
        values.append(float(transaction_amount))
    if transaction_date is not None:
        if isinstance(transaction_date, str):
            year, month, day = map(int, transaction_date.split('-'))
            transaction_date = date(year, month, day)
        updates.append("transaction_date=%s")
        values.append(transaction_date)
    if category_id is not None:
        updates.append("category_id=%s")
        values.append(category_id)

    if not updates:
        return 0

    values.append(transaction_id)
    query = f"UPDATE transactions SET {', '.join(updates)} WHERE transaction_id=%s"
    cursor.execute(query, tuple(values))
    return cursor.rowcount

def update_category(cursor, category_id, category_name):
    query = """
    UPDATE categories
    SET category_name = %s
    WHERE category_id = %s
    """

    cursor.execute(query, (category_name, category_id))
    return cursor.rowcount

