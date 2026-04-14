import tkinter as tk
from tkinter import messagebox
from connect import connect_to_sql
from insert import insert_user, insert_transactions, insert_bank_accounts, insert_budget
from delete import delete_transaction


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

def add_transaction():
    conn = connect_to_sql()
    cursor = conn.cursor()

    try:
        transaction_id = insert_transactions(
            cursor,
            int(account_id_entry.get()),
            category_dict[category_var.get()],
            transaction_name_entry.get(),
            float(amount_entry.get()),
            date_entry.get()
        )

        conn.commit()
        messagebox.showinfo("Success", f"Transaction created: {transaction_id}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

def view_budget():
    conn = connect_to_sql()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM remaining_budget WHERE budget_id=%s",
            (budget_id_entry.get(),)
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

def view_balance():
    conn = connect_to_sql()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT current_balance FROM bank_accounts WHERE account_id=%s",
            (account_id_entry.get(),)
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

def delete_tx():
    conn = connect_to_sql()
    cursor = conn.cursor()

    try:
        delete_transaction(cursor, int(transaction_id_entry.get()))
        conn.commit()

        messagebox.showinfo("Success", "Transaction deleted")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

def get_categories():
    conn = connect_to_sql()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT category_id, category_name FROM categories")

    categories = cursor.fetchall()

    cursor.close()
    conn.close()

    return categories

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

root = tk.Tk()
root.title("Budget Tracker")

# USER
tk.Label(root, text="First Name").grid(row=0, column=0)
tk.Label(root, text="Last Name").grid(row=1, column=0)
tk.Label(root, text="Email").grid(row=2, column=0)
tk.Label(root, text="Phone").grid(row=3, column=0)
tk.Label(root, text="DOB (YYYY-MM-DD)").grid(row=4, column=0)
tk.Label(root, text="Password").grid(row=5, column=0)

first_name_entry = tk.Entry(root)
last_name_entry = tk.Entry(root)
email_entry = tk.Entry(root)
phone_entry = tk.Entry(root)
dob_entry = tk.Entry(root)
password_entry = tk.Entry(root)

first_name_entry.grid(row=0, column=1)
last_name_entry.grid(row=1, column=1)
email_entry.grid(row=2, column=1)
phone_entry.grid(row=3, column=1)
dob_entry.grid(row=4, column=1)
password_entry.grid(row=5, column=1)
tk.Button(root, text="Add User", command=add_user).grid(row=6, column=0, columnspan=2)

# Bank Account
tk.Label(root, text="Bank Name").grid(row=18, column=0)
tk.Label(root, text="Account Number").grid(row=19, column=0)
tk.Label(root, text="Starting Balance").grid(row=20, column=0)
tk.Label(root, text="Account Type").grid(row=21, column=0)
tk.Label(root, text="User ID").grid(row=22, column=0)

bank_name_entry = tk.Entry(root)
account_number_entry = tk.Entry(root)
balance_entry = tk.Entry(root)
account_type_entry = tk.Entry(root)
account_user_entry = tk.Entry(root)

bank_name_entry.grid(row=18, column=1)
account_number_entry.grid(row=19, column=1)
balance_entry.grid(row=20, column=1)
account_type_entry.grid(row=21, column=1)
account_user_entry.grid(row=22, column=1)

tk.Button(root, text="Create Bank Account", command=create_account).grid(row=23, column=0, columnspan=2)

# Transactions
tk.Label(root, text="Account ID").grid(row=7, column=0)
tk.Label(root, text="Category ID").grid(row=8, column=0)
tk.Label(root, text="Transaction Name").grid(row=9, column=0)
tk.Label(root, text="Amount").grid(row=10, column=0)
tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=11, column=0)

# Budget
tk.Label(root, text="Budget User ID").grid(row=24, column=0)
tk.Label(root, text="Budget Category").grid(row=25, column=0)
tk.Label(root, text="Target Amount").grid(row=26, column=0)
tk.Label(root, text="Start Date").grid(row=27, column=0)
tk.Label(root, text="End Date").grid(row=28, column=0)

budget_user_entry = tk.Entry(root)
budget_category_entry = tk.Entry(root)
target_entry = tk.Entry(root)
start_entry = tk.Entry(root)
end_entry = tk.Entry(root)

budget_user_entry.grid(row=24, column=1)
budget_category_entry.grid(row=25, column=1)
target_entry.grid(row=26, column=1)
start_entry.grid(row=27, column=1)
end_entry.grid(row=28, column=1)

tk.Button(root, text="Create Budget", command=create_budget).grid(row=29, column=0, columnspan=2)

#Else

account_id_entry = tk.Entry(root)

categories = get_categories()

category_dict = {c['category_name']: c['category_id'] for c in categories}

category_var = tk.StringVar(root)
category_var.set(list(category_dict.keys())[0])

tk.Label(root, text="Category").grid(row=8, column=0)

category_dropdown = tk.OptionMenu(root, category_var, *category_dict.keys())
category_dropdown.grid(row=8, column=1)

transaction_name_entry = tk.Entry(root)
amount_entry = tk.Entry(root)
date_entry = tk.Entry(root)

account_id_entry.grid(row=7, column=1)
transaction_name_entry.grid(row=9, column=1)
amount_entry.grid(row=10, column=1)
date_entry.grid(row=11, column=1)

tk.Button(root, text="Add Transaction", command=add_transaction).grid(row=12, column=0, columnspan=2)

tk.Label(root, text="Budget ID").grid(row=13, column=0)
budget_id_entry = tk.Entry(root)
budget_id_entry.grid(row=13, column=1)

tk.Button(root, text="View Remaining Budget", command=view_budget).grid(row=14, column=0, columnspan=2)
tk.Button(root, text="View Account Balance", command=view_balance).grid(row=15, column=0, columnspan=2)

tk.Label(root, text="Transaction ID").grid(row=16, column=0)
transaction_id_entry = tk.Entry(root)
transaction_id_entry.grid(row=16, column=1)

tk.Button(root, text="Delete Transaction", command=delete_tx).grid(row=17, column=0, columnspan=2)

root.mainloop()