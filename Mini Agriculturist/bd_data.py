import sqlite3
from tkinter import messagebox

con = sqlite3.connect('main_database.db')
cur = con.cursor()
persons=None
try:
    query = "select More from text_data where id=0 and category='apple fruit'"
    cur.execute(query)
    persons = cur.fetchall()
    con.commit()

except Exception as e:
    messagebox.showerror("Error", str(e))

print(persons[0][0])
