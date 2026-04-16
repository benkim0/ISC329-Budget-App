import tkinter as tk
from tkinter import ttk, messagebox
from connect import connect_to_sql
from insert import insert_user, insert_transactions, insert_bank_accounts, insert_budget
from delete import delete_transaction

def run_db(action, fetch=False):
    conn = connect_to_sql()
    cursor = conn.cursor(dictionary=True)

    try:
        result = action(cursor)
        conn.commit()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        conn.close()

#Application
root = tk.Tk()
root.title("Budget App")
root.geometry("500x500")
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

#Tabs
user_frame = ttk.Frame(notebook)
bank_account_frame = ttk.Frame(notebook)
transaction_frame = ttk.Frame(notebook)
budget_frame = ttk.Frame(notebook)

notebook.add(user_frame, text="Users")
notebook.add(bank_account_frame, text="Accounts")
notebook.add(transaction_frame, text="Transactions")
notebook.add(budget_frame, text="Budgets")

# ADD USER

tk.Label(user_frame, text="First Name").grid(row=0, column=0)
tk.Label(user_frame, text="Last Name").grid(row=1, column=0)
tk.Label(user_frame, text="Email").grid(row=2, column=0)
tk.Label(user_frame, text="Phone").grid(row=3, column=0)
tk.Label(user_frame, text="DOB (YYYY-MM-DD)").grid(row=4, column=0)
tk.Label(user_frame, text="Password").grid(row=5, column=0)

first_name_entry = tk.Entry(user_frame)
last_name_entry = tk.Entry(user_frame)
email_entry = tk.Entry(user_frame)
phone_entry = tk.Entry(user_frame)
dob_entry = tk.Entry(user_frame)
password_entry = tk.Entry(user_frame)

first_name_entry.grid(row=0, column=1)
last_name_entry.grid(row=1, column=1)
email_entry.grid(row=2, column=1)
phone_entry.grid(row=3, column=1)
dob_entry.grid(row=4, column=1)
password_entry.grid(row=5, column=1)

def add_user():
    conn = connect_to_sql()
    cursor = conn.cursor()

    try:
        user_id = insert_user(
            cursor,
            first_name_entry.get(),
            last_name_entry.get(),
            email_entry.get(),
            phone_entry.get(),
            dob_entry.get(),
            password_entry.get()
        )

        conn.commit()
        messagebox.showinfo("Success", f"User created with ID {user_id}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

tk.Button(user_frame, text="Add User", command=add_user)\
    .grid(row=6, column=0, columnspan=2, pady=10)

# ADD TRANSACTIONS

def get_categories():
    conn = connect_to_sql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT category_id, category_name FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return categories
categories = get_categories() or []
category_dict = {
    c["category_name"]: c["category_id"]
    for c in categories
}
ttk.Label(transaction_frame, text="Category").grid(row=0, column=0)
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(
    transaction_frame,
    textvariable=category_var,
    values=list(category_dict.keys()),
    state="readonly"
)
category_dropdown.grid(row=0, column=1)
if category_dict:
    category_dropdown.current(0)

tk.Label(transaction_frame, text="Account ID").grid(row=1, column=0)
account_id_entry = tk.Entry(transaction_frame)
account_id_entry.grid(row=1, column=1)

tk.Label(transaction_frame, text="Transaction Name").grid(row=2, column=0)
transaction_name_entry = tk.Entry(transaction_frame)
transaction_name_entry.grid(row=2, column=1)

tk.Label(transaction_frame, text="Amount").grid(row=3, column=0)
amount_entry = tk.Entry(transaction_frame)
amount_entry.grid(row=3, column=1)

tk.Label(transaction_frame, text="Date (YYYY-MM-DD)").grid(row=4, column=0)
date_entry = tk.Entry(transaction_frame)
date_entry.grid(row=4, column=1)

def add_transaction():
    try:
        account_id = int(account_id_entry.get())
        amount = float(amount_entry.get())
        category_name = category_var.get()

        if category_name not in category_dict:
            raise ValueError("Invalid category selected")

        category_id = category_dict[category_name]

        conn = connect_to_sql()
        cursor = conn.cursor()

        try:
            transaction_id = insert_transactions(
                cursor,
                account_id,
                category_id,
                transaction_name_entry.get(),
                amount,
                date_entry.get()
            )

            conn.commit()
            messagebox.showinfo("Success", f"Transaction created: {transaction_id}")

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(
    transaction_frame,
    text="Add Transaction",
    command=add_transaction
).grid(row=6, column=0, columnspan=2, pady=10)


# ADD BANK ACCOUNTS
tk.Label(bank_account_frame, text="User ID").grid(row=0, column=0, padx=5, pady=5)
account_user_entry = tk.Entry(bank_account_frame)
account_user_entry.grid(row=0, column=1)

tk.Label(bank_account_frame, text="Bank Name").grid(row=1, column=0, padx=5, pady=5)
bank_name_entry = tk.Entry(bank_account_frame)
bank_name_entry.grid(row=1, column=1)

tk.Label(bank_account_frame, text="Account Number").grid(row=2, column=0, padx=5, pady=5)
account_number_entry = tk.Entry(bank_account_frame)
account_number_entry.grid(row=2, column=1)

tk.Label(bank_account_frame, text="Starting Balance").grid(row=3, column=0, padx=5, pady=5)
balance_entry = tk.Entry(bank_account_frame)
balance_entry.grid(row=3, column=1)

tk.Label(bank_account_frame, text="Account Type").grid(row=4, column=0, padx=5, pady=5)
account_type_entry = tk.Entry(bank_account_frame)
account_type_entry.grid(row=4, column=1)

def create_account():
    conn = connect_to_sql()
    cursor = conn.cursor()

    try:
        account_id = insert_bank_accounts(
            cursor,
            int(account_user_entry.get()),
            bank_name_entry.get(),
            int(account_number_entry.get()),
            float(balance_entry.get()),
            account_type_entry.get()
        )

        conn.commit()
        messagebox.showinfo("Success", f"Account created: {account_id}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

tk.Button(
    bank_account_frame,
    text="Create Account",
    command=create_account
).grid(row=5, column=0, columnspan=2, pady=10)

# ADD BUDGET

tk.Label(budget_frame, text="User ID").grid(row=0, column=0, padx=5, pady=5)
budget_user_entry = tk.Entry(budget_frame)
budget_user_entry.grid(row=0, column=1)

tk.Label(budget_frame, text="Category ID").grid(row=1, column=0, padx=5, pady=5)
budget_category_entry = tk.Entry(budget_frame)
budget_category_entry.grid(row=1, column=1)

tk.Label(budget_frame, text="Target Amount").grid(row=2, column=0, padx=5, pady=5)
target_entry = tk.Entry(budget_frame)
target_entry.grid(row=2, column=1)

tk.Label(budget_frame, text="Start Date (YYYY-MM-DD)").grid(row=3, column=0, padx=5, pady=5)
start_entry = tk.Entry(budget_frame)
start_entry.grid(row=3, column=1)

tk.Label(budget_frame, text="End Date (YYYY-MM-DD)").grid(row=4, column=0, padx=5, pady=5)
end_entry = tk.Entry(budget_frame)
end_entry.grid(row=4, column=1)

tk.Label(budget_frame, text="Budget ID").grid(row=6, column=0, padx=5, pady=5)
budget_id_entry = tk.Entry(budget_frame)
budget_id_entry.grid(row=6, column=1)


def create_budget():
    conn = connect_to_sql()
    cursor = conn.cursor()

    try:
        budget_id = insert_budget(
            cursor,
            int(budget_user_entry.get()),
            int(budget_category_entry.get()),
            float(target_entry.get()),
            start_entry.get(),
            end_entry.get()
        )

        conn.commit()
        messagebox.showinfo("Success", f"Budget created: {budget_id}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

tk.Button(
    budget_frame,
    text="Create Budget",
    command=create_budget
).grid(row=5, column=0, columnspan=2, pady=10)

#DELETE TRANSACTION

tk.Label(transaction_frame, text="Transaction ID").grid(row=7, column=0)
delete_entry = tk.Entry(transaction_frame)
delete_entry.grid(row=7, column=1)

def delete_transaction():
    try:
        transaction_id = int(delete_entry.get())

        conn = connect_to_sql()
        cursor = conn.cursor()

        try:
            delete_transaction(cursor, transaction_id)
            conn.commit()
            messagebox.showinfo("Success", "Transaction deleted")
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


tk.Button(
    transaction_frame,
    text="Delete Transaction",
    command=delete_transaction
).grid(row=8, column=0, columnspan=2, pady=5)

# VIEW BALANCE

def view_balance():
    try:
        account_id = int(account_id_entry.get())

        conn = connect_to_sql()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT current_balance FROM bank_accounts WHERE account_id=%s",
                (account_id,)
            )

            result = cursor.fetchone()

            if result:
                messagebox.showinfo(
                    "Account Balance",
                    f"Balance: {result['current_balance']}"
                )
            else:
                messagebox.showinfo("Result", "Account not found")
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Label(bank_account_frame, text="Account ID").grid(row=6, column=0, padx=5, pady=5)

account_id_entry = tk.Entry(bank_account_frame)
account_id_entry.grid(row=6, column=1)

tk.Button(
    bank_account_frame,
    text="View Balance",
    command=view_balance
).grid(row=7, column=0, columnspan=2, pady=10)

#VIEW BUDGET

def view_budget():
    try:
        budget_id = int(budget_id_entry.get())

        conn = connect_to_sql()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM remaining_budget WHERE budget_id=%s",
                (budget_id,)
            )

            result = cursor.fetchone()

            if result:
                messagebox.showinfo(
                    "Budget Info",
                    f"Target: {result['target_amount']}\n"
                    f"Spent: {result['amount_spent']}\n"
                    f"Remaining: {result['remaining_balance']}"
                )
            else:
                messagebox.showinfo("Result", "Budget not found")

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(
    budget_frame,
    text="View Budget",
    command=view_budget
).grid(row=7, column=0, columnspan=2, pady=10)

#RUN
root.mainloop()
