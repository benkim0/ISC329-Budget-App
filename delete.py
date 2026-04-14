def delete_user(cursor, user_id):
    query = """
    DELETE FROM user
    WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    return cursor.rowcount

def delete_bank_account(cursor, account_id):
    query = """
    DELETE FROM bank_accounts
    WHERE account_id = %s
    """
    cursor.execute(query, (account_id,))
    return cursor.rowcount

def delete_budget(cursor, budget_id):
    query = """
    DELETE FROM budget
    WHERE budget_id = %s
    """
    cursor.execute(query, (budget_id,))
    return cursor.rowcount

def delete_category(cursor, category_id):
    query = """
    DELETE FROM categories
    WHERE category_id = %s
    """
    cursor.execute(query, (category_id,))
    return cursor.rowcount

def delete_transaction(cursor, transaction_id):
    query = """
    DELETE FROM transactions
    WHERE transaction_id = %s
    """
    cursor.execute(query, (transaction_id,))
    return cursor.rowcount

