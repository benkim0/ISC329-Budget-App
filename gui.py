# #DELETE BANK ACCOUNT
# tk.Label(bank_account_frame, text="Bank Account ID").grid(row=8, column=0)
# delete_ba_entry = tk.Entry(bank_account_frame)
# delete_ba_entry.grid(row=8, column=1)
#
# def delete_ba():
#     try:
#         bank_account_id = int(delete_ba_entry.get())
#
#         conn = connect_to_sql()
#         cursor = conn.cursor()
#
#         try:
#             delete_bank_account(cursor, bank_account_id)
#             conn.commit()
#             messagebox.showinfo("Success", "Bank Account deleted")
#         finally:
#             cursor.close()
#             conn.close()
#
#     except Exception as e:
#         messagebox.showerror("Error", str(e))
#
# tk.Button(
#     bank_account_frame,
#     text="Delete Bank Account",
#     command=delete_ba
# ).grid(row=9, column=0, columnspan=2, pady=5)
#
# #DELETE BUDGET
# tk.Label(budget_frame, text="Budget ID (Delete)").grid(row=9, column=0)
# delete_bud_entry = tk.Entry(budget_frame)
# delete_bud_entry.grid(row=9, column=1)
#
# def delete_bud():
#     try:
#         budget_id = int(delete_bud_entry.get())
#
#         conn = connect_to_sql()
#         cursor = conn.cursor()
#
#         try:
#             delete_budget(cursor, budget_id)
#             conn.commit()
#             messagebox.showinfo("Success", "Budget deleted")
#         finally:
#             cursor.close()
#             conn.close()
#
#     except Exception as e:
#         messagebox.showerror("Error", str(e))
#
# tk.Button(
#     budget_frame,
#     text="Delete Budget",
#     command=delete_bud
# ).grid(row=10, column=0, columnspan=2, pady=5)