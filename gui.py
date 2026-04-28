import tkinter as tk
from tkinter import ttk, messagebox
from connect import connect_to_sql
from insert import insert_user, insert_transactions, insert_bank_accounts, insert_budget
from delete import delete_transaction, delete_user, delete_bank_account, delete_budget

current_user_id = None

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
login_frame = ttk.Frame(notebook)

notebook.add(login_frame, text="Login")
notebook.add(user_frame, text="Users")
notebook.add(bank_account_frame, text="Accounts")
notebook.add(transaction_frame, text="Transactions")
notebook.add(budget_frame, text="Budgets")

#LOGIN
tk.Label(login_frame, text="Email").grid(row=0, column=0)
tk.Label(login_frame, text="Password").grid(row=1, column=0)

login_email_entry = tk.Entry(login_frame)
login_password_entry = tk.Entry(login_frame, show="*")

login_email_entry.grid(row=0, column=1)
login_password_entry.grid(row=1, column=1)

def login():
    global current_user_id

    email = login_email_entry.get()
    password = login_password_entry.get()

    conn = connect_to_sql()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT user_id FROM user WHERE email_address=%s AND password=%s",
            (email, password)
        )

        result = cursor.fetchone()

        if result:
            current_user_id = result["user_id"]
            messagebox.showinfo("Success", "Logged in!")

            notebook.tab(1, state="normal")
            notebook.tab(2, state="normal")
            notebook.tab(3, state="normal")
            notebook.tab(4, state="normal")
            notebook.select(1)

            accounts = get_user_accounts()
            account_dict = {
                f"{a['bank_name']} (ID:{a['account_id']})": a['account_id']
                for a in accounts
            }
            account_dropdown["values"] = list(account_dict.keys())
            if account_dict:
                account_var.set(list(account_dict.keys())[0])

            budgets = get_user_budgets()
            budget_dict = {
                f"{b['category_name']}: {str(b['start_date'])} → {str(b['end_date'])} (ID:{b['budget_id']})": b['budget_id']
                for b in budgets
            }
            budget_dropdown["values"] = list(budget_dict.keys())
            if budget_dict:
                budget_var.set(list(budget_dict.keys())[0])

        else:
            messagebox.showerror("Error", "Invalid login")

    finally:
        cursor.close()
        conn.close()

tk.Button(login_frame, text="Login", command=login).grid(row=2, column=0, columnspan=2)

# ADD USER

signup_frame = tk.Frame(login_frame)
signup_frame.grid(row=3, column=0, columnspan=2)
signup_frame.grid_remove()

tk.Label(signup_frame, text="First Name").grid(row=0, column=0)
tk.Label(signup_frame, text="Last Name").grid(row=1, column=0)
tk.Label(signup_frame, text="Email").grid(row=2, column=0)
tk.Label(signup_frame, text="Phone").grid(row=3, column=0)
tk.Label(signup_frame, text="DOB (YYYY-MM-DD)").grid(row=4, column=0)
tk.Label(signup_frame, text="Password").grid(row=5, column=0)

first_name_entry = tk.Entry(signup_frame)
last_name_entry = tk.Entry(signup_frame)
email_entry = tk.Entry(signup_frame)
phone_entry = tk.Entry(signup_frame)
dob_entry = tk.Entry(signup_frame)
password_entry = tk.Entry(signup_frame)

first_name_entry.grid(row=0, column=1)
last_name_entry.grid(row=1, column=1)
email_entry.grid(row=2, column=1)
phone_entry.grid(row=3, column=1)
dob_entry.grid(row=4, column=1)
password_entry.grid(row=5, column=1)

def show_signup():
    signup_frame.grid()

def hide_signup():
    signup_frame.grid_remove()

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

tk.Button(signup_frame, text="Add User", command=add_user)\
    .grid(row=6, column=0, columnspan=2, pady=10)

tk.Button(login_frame, text="New user? Sign up", command=show_signup)\
    .grid(row=10, column=0, columnspan=2)

tk.Button(signup_frame, text="Back to login", command=hide_signup)\
    .grid(row=7, column=0, columnspan=2)

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
        category_name = category_dropdown.get().strip()

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

tk.Label(bank_account_frame, text="Bank Name").grid(row=0, column=0, padx=5, pady=5)
bank_name_entry = tk.Entry(bank_account_frame)
bank_name_entry.grid(row=0, column=1)

tk.Label(bank_account_frame, text="Account Number").grid(row=1, column=0, padx=5, pady=5)
account_number_entry = tk.Entry(bank_account_frame)
account_number_entry.grid(row=1, column=1)

tk.Label(bank_account_frame, text="Starting Balance").grid(row=2, column=0, padx=5, pady=5)
balance_entry = tk.Entry(bank_account_frame)
balance_entry.grid(row=2, column=1)

tk.Label(bank_account_frame, text="Account Type").grid(row=3, column=0, padx=5, pady=5)
account_type_entry = tk.Entry(bank_account_frame)
account_type_entry.grid(row=3, column=1)

def create_account():
    global current_user_id

    conn = connect_to_sql()
    cursor = conn.cursor()

    try:
        account_id = insert_bank_accounts(
            cursor,
            current_user_id,
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
).grid(row=4, column=0, columnspan=2, pady=10)

# ADD BUDGET

ttk.Label(budget_frame, text="Category").grid(row=0, column=0)
budget_categories = get_categories() or []
budget_category_dict = {
    c["category_name"]: c["category_id"]
    for c in categories
}
budget_category_var = tk.StringVar()
budget_category_dropdown = ttk.Combobox(
    budget_frame,
    textvariable=budget_category_var,
    values=list(budget_category_dict.keys()),
    state="readonly"
)
budget_category_dropdown.grid(row=0, column=1)
if budget_category_dict:
    budget_category_dropdown.current(0)

tk.Label(budget_frame, text="Target Amount").grid(row=1, column=0, padx=5, pady=5)
target_entry = tk.Entry(budget_frame)
target_entry.grid(row=1, column=1)

tk.Label(budget_frame, text="Start Date (YYYY-MM-DD)").grid(row=2, column=0, padx=5, pady=5)
start_entry = tk.Entry(budget_frame)
start_entry.grid(row=2, column=1)

tk.Label(budget_frame, text="End Date (YYYY-MM-DD)").grid(row=3, column=0, padx=5, pady=5)
end_entry = tk.Entry(budget_frame)
end_entry.grid(row=3, column=1)

def create_budget():
    conn = connect_to_sql()
    cursor = conn.cursor()

    budget_category_name = budget_category_var.get()
    if budget_category_name not in budget_category_dict:
        raise ValueError("Invalid category selected")
    budget_category_id = budget_category_dict[budget_category_name]

    try:
        budget_id = insert_budget(
            cursor,
            current_user_id,
            budget_category_id,
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
delete_tr_entry = tk.Entry(transaction_frame)
delete_tr_entry.grid(row=7, column=1)

def delete_tr():
    try:
        transaction_id = int(delete_tr_entry.get())

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
    command=delete_tr
).grid(row=8, column=0, columnspan=2, pady=5)

# VIEW BALANCE

def get_user_accounts():
    global current_user_id

    conn = connect_to_sql()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT account_id, bank_name FROM bank_accounts WHERE user_id=%s",
        (current_user_id,)
    )

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def view_balance():
    global current_user_id

    try:
        account_label = account_var.get()
        account_id = int(account_label.split("ID:")[1].replace(")", ""))

        conn = connect_to_sql()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT current_balance FROM bank_accounts WHERE account_id=%s AND user_id = %s",
                (account_id, current_user_id)
            )

            result = cursor.fetchone()

            if result:
                messagebox.showinfo(
                    "Account Balance",
                    f"Balance: {result['current_balance']}"
                )
            else:
                messagebox.showinfo("Result", "Account not found or not yours")
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

account_var = tk.StringVar()
account_dict = {}

account_dropdown = ttk.Combobox(
    bank_account_frame,
    textvariable=account_var,
    values=list(account_dict.keys()),
    state="readonly"
)

tk.Label(bank_account_frame, text="Choose Account").grid(row=6, column=0)
account_dropdown.grid(row=6, column=1)

tk.Button(
    bank_account_frame,
    text="View Balance",
    command=view_balance
).grid(row=7, column=0, columnspan=2, pady=10)

#VIEW BUDGET

def get_user_budgets():
    conn = connect_to_sql()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT b.user_id, b.budget_id, c.category_name, b.target_amount, b.start_date, b.end_date FROM budget b JOIN categories c ON b.category_id = c.category_id WHERE b.user_id = %s",
        (current_user_id,)
    )

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def view_budget():
    global current_user_id

    try:
        budget_label = budget_var.get()
        budget_id = int(budget_label.split("ID:")[1].replace(")", ""))

        conn = connect_to_sql()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT rb.*
                FROM remaining_budget rb
                JOIN budget b ON rb.budget_id = b.budget_id
                WHERE rb.budget_id = %s
                AND b.user_id = %s
            """, (budget_id, current_user_id))

            result = cursor.fetchone()

            if result:
                messagebox.showinfo(
                    "Budget Info",
                    f"Target: {result['target_amount']}\n"
                    f"Spent: {result['amount_spent']}\n"
                    f"Remaining: {result['remaining_balance']}"
                )
            else:
                messagebox.showinfo("Result", "Budget not yours or not found")

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

budget_var = tk.StringVar()
budget_dict = {}

budget_dropdown = ttk.Combobox(
    budget_frame,
    textvariable=budget_var,
    values=[],
    state="readonly",
    width= 50
)

tk.Label(budget_frame, text="Choose Budget").grid(row=7, column=0)
budget_dropdown.grid(row=7, column=1)

tk.Button(
    budget_frame,
    text="View Budget",
    command=view_budget
).grid(row=8, column=0, columnspan=2, pady=10)

#DELETE USER

tk.Label(user_frame, text="User ID").grid(row=7, column=0)
delete_us_entry = tk.Entry(user_frame)
delete_us_entry.grid(row=7, column=1)

def delete_us():
    try:
        user_id = int(delete_us_entry.get())

        conn = connect_to_sql()
        cursor = conn.cursor()

        try:
            delete_user(cursor, user_id)
            conn.commit()
            messagebox.showinfo("Success", "User deleted")
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(
    user_frame,
    text="Delete User",
    command=delete_us
).grid(row=8, column=0, columnspan=2, pady=5)

#DELETE BANK ACCOUNT

tk.Label(bank_account_frame, text="Bank Account ID").grid(row=8, column=0)
delete_ba_entry = tk.Entry(bank_account_frame)
delete_ba_entry.grid(row=8, column=1)

def delete_ba():
    try:
        bank_account_id = int(delete_ba_entry.get())

        conn = connect_to_sql()
        cursor = conn.cursor()

        try:
            delete_bank_account(cursor, bank_account_id)
            conn.commit()
            messagebox.showinfo("Success", "Bank Account deleted")
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(
    bank_account_frame,
    text="Delete Bank Account",
    command=delete_ba
).grid(row=9, column=0, columnspan=2, pady=5)

#DELETE BUDGET
tk.Label(budget_frame, text="Budget ID (Delete)").grid(row=9, column=0)
delete_bud_entry = tk.Entry(budget_frame)
delete_bud_entry.grid(row=9, column=1)

def delete_bud():
    try:
        budget_id = int(delete_bud_entry.get())

        conn = connect_to_sql()
        cursor = conn.cursor()

        try:
            delete_budget(cursor, budget_id)
            conn.commit()
            messagebox.showinfo("Success", "Budget deleted")
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(
    budget_frame,
    text="Delete Budget",
    command=delete_bud
).grid(row=10, column=0, columnspan=2, pady=5)

#RUN

notebook.select(0)
notebook.tab(1, state="disabled")
notebook.tab(2, state="disabled")
notebook.tab(3, state="disabled")
notebook.tab(4, state="disabled")
root.mainloop()