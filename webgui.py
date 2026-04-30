from flask import Flask, render_template, request, redirect, session, flash
from connect import connect_to_sql
from insert import insert_user, insert_transactions, insert_bank_accounts, insert_budget
from delete import delete_transaction, delete_user, delete_bank_account, delete_budget
from update import update_user
import os

app = Flask(__name__)
app.secret_key = "dev-key"
current_user_id = None


def run_db(action):
    conn = connect_to_sql()
    if conn is None:
        return "DB error", 500
    cursor = conn.cursor(dictionary=True)

    try:
        result = action(cursor)
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


@app.route("/")
def home():
    return redirect("/login")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = connect_to_sql()
        if conn is None:
            return "DB error", 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_id FROM user WHERE email_address=%s AND password=%s",
            (email, password)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            session["user_id"] = result["user_id"]
            return redirect("/dashboard")
        flash("Invalid login")
        return redirect("/login")
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        conn = connect_to_sql()
        if conn is None:
            return "DB error", 500
        cursor = conn.cursor()
        try:
            user_id = insert_user(
                cursor,
                request.form["first_name"],
                request.form["last_name"],
                request.form["email"],
                request.form["phone"],
                request.form["dob"],
                request.form["password"]
            )
            conn.commit()
            flash(f"User created with ID {user_id}")
            return redirect("/login")
        except Exception as e:
            flash(str(e))
            return redirect("/signup")
        finally:
            cursor.close()
            conn.close()
    return render_template("signup.html")


# Transactions
@app.route("/transactions")
def transactions():
    if "user_id" not in session:
        return redirect("/login")
    sort = request.args.get("sort", "date")
    order_by = {
        "date": "t.transaction_date DESC",
        "name": "t.transaction_name",
        "amount": "t.transaction_amount DESC"
    }[sort]
    conn = connect_to_sql()
    if conn is None:
        return "DB error", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"""
        SELECT t.transaction_id, t.transaction_date, t.transaction_name, t.transaction_amount
        FROM transactions t
        JOIN bank_accounts b ON t.account_id = b.account_id
        WHERE b.user_id = %s
        ORDER BY {order_by}
    """, (session["user_id"],))
    transactions = cursor.fetchall()
    cursor.execute("""
        SELECT account_id, bank_name
        FROM bank_accounts
        WHERE user_id=%s
    """, (session["user_id"],))
    accounts = cursor.fetchall()
    cursor.execute("""
        SELECT category_id, category_name
        FROM categories
    """)
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template(
        "transactions.html",
        transactions=transactions,
        accounts=accounts,
        categories=categories,
        sort=sort
    )


@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    if "user_id" not in session:
        return redirect("/login")
    conn = connect_to_sql()
    if conn is None:
        return "DB error", 500
    cursor = conn.cursor()
    try:
        insert_transactions(
            cursor,
            request.form["account_id"],
            request.form["category_id"],
            request.form["name"],
            float(request.form["amount"]),
            request.form["date"]
        )
        conn.commit()
        flash("Transaction added")
    except Exception as e:
        flash(str(e))
    finally:
        cursor.close()
        conn.close()
    return redirect("/transactions")


@app.route("/delete_transaction/<int:transaction_id>")
def delete_transaction_route(transaction_id):
    if "user_id" not in session:
        return redirect("/login")
    conn = connect_to_sql()
    if conn is None:
        return "DB error", 500
    cursor = conn.cursor()
    try:
        delete_transaction(cursor, transaction_id, session["user_id"])
        conn.commit()
        flash("Transaction deleted")
    except Exception as e:
        flash(str(e))
    finally:
        cursor.close()
        conn.close()
    return redirect("/transactions")


@app.route("/accounts", methods=["GET"])
def accounts():
    if "user_id" not in session:
        return redirect("/login")
    conn = connect_to_sql()
    if conn is None:
        return "DB error", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT account_id, bank_name
        FROM bank_accounts
        WHERE user_id = %s
    """, (session["user_id"],))
    accounts = cursor.fetchall()
    account_id = request.args.get("account_id")
    balance = None
    if account_id:
        cursor.execute("""
            SELECT current_balance
            FROM bank_accounts
            WHERE account_id = %s AND user_id = %s
        """, (account_id, session["user_id"]))
        result = cursor.fetchone()
        if result:
            balance = result["current_balance"]
    cursor.close()
    conn.close()
    return render_template(
        "accounts.html",
        accounts=accounts,
        balance=balance,
        selected_account=account_id
    )


@app.route("/add_account", methods=["POST"])
def add_account():
    if "user_id" not in session:
        return redirect("/login")
    conn = connect_to_sql()
    if conn is None:
        return "DB error", 500
    cursor = conn.cursor()
    try:
        insert_bank_accounts(
            cursor,
            session["user_id"],
            request.form["bank_name"],
            int(request.form["account_number"]),
            float(request.form["balance"]),
            request.form["account_type"]
        )
        conn.commit()
        flash("Account created successfully!")
    except Exception as e:
        flash(str(e))
    finally:
        cursor.close()
        conn.close()
    return redirect("/accounts")


@app.route("/budgets", methods=["GET"])
def budgets():
    if "user_id" not in session:
        return redirect("/login")
    conn = connect_to_sql()
    if conn is None:
        return "DB error", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.budget_id, c.category_name, b.start_date, b.end_date
        FROM budget b
        JOIN categories c ON b.category_id = c.category_id
        WHERE b.user_id = %s
    """, (session["user_id"],))
    budgets = cursor.fetchall()
    budget_id = request.args.get("budget_id")
    budget_data = None
    if budget_id:
        cursor.execute("""
            SELECT rb.target_amount,
                   rb.amount_spent,
                   rb.remaining_balance
            FROM remaining_budget rb
            JOIN budget b ON rb.budget_id = b.budget_id
            WHERE rb.budget_id = %s
            AND b.user_id = %s
        """, (budget_id, session["user_id"]))
        budget_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template(
        "budgets.html",
        budgets=budgets,
        budget_data=budget_data,
        selected_budget=budget_id
    )


@app.route("/add_budget", methods=["POST"])
def add_budget():
    if "user_id" not in session:
        return redirect("/login")
    conn = connect_to_sql()
    if conn is None:
        return "DB error", 500
    cursor = conn.cursor()
    try:
        insert_budget(
            cursor,
            session["user_id"],
            request.form["category_id"],
            float(request.form["target_amount"]),
            request.form["start_date"],
            request.form["end_date"]
        )
        conn.commit()
        flash("Budget created successfully!")
    except Exception as e:
        flash(str(e))
    finally:
        cursor.close()
        conn.close()
    return redirect("/budgets")


@app.route("/users", methods=["GET", "POST"])
def users():
    if "user_id" not in session:
        return redirect("/login")
    user_id = session["user_id"]
    if request.method == "POST":
        conn = connect_to_sql()
        if conn is None:
            return "DB error", 500
        cursor = conn.cursor()
        try:
            update_user(
                cursor,
                user_id,
                request.form.get("first_name"),
                request.form.get("last_name"),
                request.form.get("email"),
                request.form.get("phone"),
                request.form.get("dob"),
                request.form.get("password")
            )
            conn.commit()
            flash("User updated successfully")
            return redirect("/users")
        finally:
            cursor.close()
            conn.close()
    return render_template("user_settings.html")


@app.route("/delete_user", methods=["POST"])
def delete_account():
    if "user_id" not in session:
        return redirect("/login")
    user_id = session["user_id"]
    conn = connect_to_sql()
    if conn is None:
        return "DB error", 500
    cursor = conn.cursor()
    try:
        delete_user(cursor, user_id)
        conn.commit()
        session.clear()
        flash("Account deleted successfully")
        return redirect("/login")
    finally:
        cursor.close()
        conn.close()



