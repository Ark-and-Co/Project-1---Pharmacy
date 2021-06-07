from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tabulate import tabulate
from datetime import datetime
import pandas as pd
import sqlite3

'''
Root Window:
    main_frame:
        my_canvas:
            main_window:
                search_frame:
                    search_label
                    search_box
                    search_now_button
                    lable1_label
                database_tree_frame:
                    database_tree
                record_frame:
                    ID_label
                    id_entry_box
                    medicine_name_label
                    medicine_name_box
                    medicine_Stock_label
                    medicine_stock_box
                    medicine_price_label
                    medicine_price_box
                commands_frame:
                    update_button
                    add_record_button
                    remove_one_button
                    clear_button
                account_search_frame:
                    account_search_label
                    account_search_box
                    account_count_label
                    account_count_box
                    label2_label
                account_tree_frame:
                    account_tree
                account_details_frame:
                    remove one button
                    account_now_button:
                        accounting_window:
                            accounting_details_frame:

                            accounting_tree_frame:
                                accounting_tree
                            accounting_prices_frame:

                transaction_register_frame:
                    open transaction register_button:
                        transaction register window:
                            daily_transaction_tree_Frame:
                                daily_transaction_tree
                            daily_date_tree_frame:
                                daily_date_tree
                            all_transaction_tree_frame:
                                all_transaction_tree
                            monthly_date_tree_frame:
                                monthly_date_tree
                            year_date_tree_frame:
                                year_date_tree
                            medicine_database_view_tree_frame:
                                medicine_database_view_tree
                            button_frame:
                                refresh_now_button
                                drop_box_asc_desc
                                drop_box_name_count_price
'''
# ---------------------------------------------<Root Window>------------------------------------------------------------
root = Tk()
root.title('Database Pharmacy')
background_color = 'lightblue'
root.geometry('1920x1080')
# Create A Main Frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

# Create A Canvas
my_canvas = Canvas(main_frame)
my_canvas.configure(background=background_color)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Add A Scrollbar To The Canvas
my_scrollbar_y = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar_y.pack(side=RIGHT, fill=Y)

# Configure The Canvas
my_canvas.configure(yscrollcommand=my_scrollbar_y.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))


def _on_mouse_wheel(event):
    my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")


my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

# Create ANOTHER Frame INSIDE the Canvas
main_window = Frame(my_canvas)
main_window.configure(background=background_color)

# Add that New frame To a Window In The Canvas
my_canvas.create_window((0, 0), window=main_window, anchor="nw")
# ---------------------------------------------</Root window>-----------------------------------------------------------
# ---------------------------------------------<Global variables>-------------------------------------------------------
transaction_details = []
item_id = []
medicine_data_path = 'medicine_data.csv'
transaction_data_path = 'transaction_data.csv'

# ---------------------------------------------</Global variables>------------------------------------------------------
# ---------------------------------------------<Transactions Database commit>-------------------------------------------


def transaction_commit():
    conn = sqlite3.connect('pharmacy.db')

    # Create a cursor instance
    c = conn.cursor()

    # Add New Record
    c.execute("INSERT INTO transactions VALUES (:name, :date, :id, :count, :total)",
              {
                  'name': transaction_details[0][0],
                  'date': transaction_details[0][1],
                  'id': transaction_details[0][2],
                  'count': transaction_details[0][3],
                  'total': transaction_details[0][4]

              })

    # Commit changes
    conn.commit()

    conn.close()
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM transactions')

        sql_query = pd.read_sql_query("SELECT * FROM transactions", conn)

        df = pd.DataFrame(sql_query)
        df.to_csv(transaction_data_path, index=False)

        print('Saved all transaction data!')

    except Exception:
        messagebox.showinfo('File Open', 'Close your file to view saved data!')

    return
# ---------------------------------------------</Transactions Database commit>------------------------------------------
# ---------------------------------------------<Medicine/Transactions Database INIT>------------------------------------


conn = sqlite3.connect('pharmacy.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE if not exists medicine (
medicine_id integer AUTO INCREMENT PRIMARY KEY,
medicine_name text UNIQUE,
medicine_stock integer,
medicine_price integer)''')
cursor.execute('''CREATE TABLE if not exists transactions (
patient_name text,
transaction_date text,
transaction_id text,
transaction_count text,
transaction_total integer)''')

conn.close()
# ---------------------------------------------</Medicine/Transactions Database INIT>-----------------------------------
# ---------------------------------------------<Medicine Database SQL Functions>----------------------------------------


def show_table():
    conn = sqlite3.connect('pharmacy.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicine")
    record = cursor.fetchall()
    list = []
    for records in record:
        list.append([records[0], records[1], records[2], records[3]])

    headers = ('Item ID', 'Item Name', 'Item Stock', 'Item Price')
    table = tabulate(list, headers, tablefmt="grid")

    print(table)


def update_row(id, name, stock, price):
    conn = sqlite3.connect('pharmacy.db')
    cursor = conn.cursor()
    sql = "UPDATE medicine SET  medicine_name = ? , medicine_stock= ? , medicine_price = ?  WHERE medicine_id = ?"
    val = (name, stock, price, id)
    cursor.execute(sql, val)
    conn.commit()
    conn.close()


show_table()


def query_database():
    global item_id
    item_id.clear()
    # Create a database or connect to one that exists
    conn = sqlite3.connect('pharmacy.db')

    # Create a cursor instance
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM medicine")
    records = c.fetchall()

    # Add our data to the screen

    count = 0

    for record in records:
        item_id.append(record[0])

        if count % 2 == 0:
            database_tree.insert(parent='', index='end', iid=count, text='',
                                 values=(record[1], record[2], record[3], record[4]),
                                 tags=('evenrow',))
        else:
            database_tree.insert(parent='', index='end', iid=count, text='',
                                 values=(record[1], record[2], record[3], record[4]),
                                 tags=('oddrow',))
        # increment counter
        count += 1

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()
    try:
        conn = sqlite3.connect('pharmacy.db')

        sql_query = pd.read_sql_query("SELECT * FROM medicine", conn)

        df = pd.DataFrame(sql_query)

        df.to_csv(medicine_data_path, index=False)
        print('Saved all Medicine data!')
    except Exception:
        messagebox.showinfo('File Open', 'Close your file to view saved data!')

# ---------------------------------------------</Medicine Database SQL Functions>---------------------------------------
#  -------------------------------------------------<Main window Frames>------------------------------------------------


tree_frame = Frame(main_window)
tree_frame.grid(row=1, column=0, padx=20)
tree_frame.configure(background=background_color)

search_frame = LabelFrame(main_window, text="Search")
search_frame.grid(row=0, column=0, padx=20)
search_frame.configure(background=background_color)
# search_frame.pack(fill="x", expand="yes", padx=20)

data_frame = LabelFrame(main_window, text="Record")
data_frame.grid(row=2, column=0, pady=20, padx=20)
data_frame.configure(background=background_color)
# data_frame.pack(fill="x", expand="yes", padx=20)

button_frame = LabelFrame(main_window, text="Commands")
button_frame.grid(row=3, column=0, pady=20, padx=20)
button_frame.configure(background=background_color)
# button_frame.pack(fill="x", expand="yes", padx=20)

account_search_frame = LabelFrame(main_window, text="Account Search")
account_search_frame.grid(row=0, column=1, pady=20, padx=20)
account_search_frame.configure(background=background_color)

account_tree_frame = Frame(main_window)
account_tree_frame.grid(row=1, column=1, pady=20, padx=20)

account_options_frame = LabelFrame(main_window, text="Account Options")
account_options_frame.grid(row=2, column=1, pady=20, padx=20)
account_options_frame.configure(background=background_color)

transaction_register_frame = LabelFrame(main_window, text="Transaction Register")
transaction_register_frame.grid(row=3, column=1, pady=20, padx=20)
transaction_register_frame.configure(background=background_color)

#  -------------------------------------------------</Main window Frames>-----------------------------------------------
#  -------------------------------------------------<Database Treeview options>-----------------------------------------

# Add Some Style
style = ttk.Style()

# Pick A Theme
style.theme_use('default')

# Configure the Treeview Colors
style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")

# Change Selected Color
style.map('Treeview',
          background=[('selected', "#347083")])

database_tree_scroll = Scrollbar(tree_frame)
database_tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
database_tree = ttk.Treeview(tree_frame, yscrollcommand=database_tree_scroll.set, selectmode="extended")
database_tree.pack()

# Configure the Scrollbar
database_tree_scroll.config(command=database_tree.yview)

# Define Our Columns
database_tree['columns'] = ("ID", "Medicine Name", "Medicine Stock", "Medicine Price")

# Format Our Columns
database_tree.column("#0", width=0, stretch=NO)
database_tree.column("ID", anchor=CENTER, width=100)
database_tree.column("Medicine Name", anchor=W, width=140)
database_tree.column("Medicine Stock", anchor=CENTER, width=140)
database_tree.column("Medicine Price", anchor=W, width=140)

# Create Headings
database_tree.heading("#0", text="", anchor=W)
database_tree.heading("ID", text="ID", anchor=W)
database_tree.heading("Medicine Name", text="Medicine Name", anchor=W)
database_tree.heading("Medicine Stock", text="Medicine Stock", anchor=CENTER)
database_tree.heading("Medicine Price", text="Medicine Price", anchor=CENTER)

# Create Striped Row Tags
database_tree.tag_configure('oddrow', background="white")
database_tree.tag_configure('evenrow', background="lightblue")
#  -------------------------------------------------</Database Treeview options>----------------------------------------
#  -------------------------------------------------<Database Treeview functions>---------------------------------------

# Remove one record


def remove_one():
    try:
        x = database_tree.selection()[0]
        database_tree.delete(x)

        # Create a database or connect to one that exists
        conn = sqlite3.connect('pharmacy.db')

        # Create a cursor instance
        c = conn.cursor()

        # Delete From Database
        c.execute("DELETE from medicine WHERE oid=" + id_entry_box.get())

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

        # Clear The Entry Boxes
        clear_entries()

        # Add a little message box for fun
        messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")
    except Exception:
        messagebox.showinfo("Error", "You have not selected a row to remove")


# Clear entry boxes
def clear_entries():
    # Clear entry boxes
    id_entry_box.delete(0, END)
    name_entry_box.delete(0, END)
    stock_entry_box.delete(0, END)
    price_entry_box.delete(0, END)


# Select Record
def select_record(e):
    # Clear entry boxes
    id_entry_box.delete(0, END)
    name_entry_box.delete(0, END)
    stock_entry_box.delete(0, END)
    price_entry_box.delete(0, END)

    # Grab record Number
    selected = database_tree.focus()
    # Grab record values
    values = database_tree.item(selected, 'values')
    print(values[0])
    print(values[1])
    print(values[2])
    print(values[3])
    print("\n")

    # output to entry boxes
    id_entry_box.insert(0, values[0])
    name_entry_box.insert(0, values[1])
    stock_entry_box.insert(0, values[2])
    price_entry_box.insert(0, values[3])


# Update record
def update_record():
    try:
        # Update the database
        # Create a database or connect to one that exists
        conn = sqlite3.connect('pharmacy.db')

        # Create a cursor instance
        c = conn.cursor()

        c.execute("""UPDATE medicine SET
            medicine_name = :name,
            medicine_stock = :stock,
            medicine_price = :price
            WHERE medicine_id = :oid""",
                  {
                      'name': name_entry_box.get(),
                      'stock': stock_entry_box.get(),
                      'price': price_entry_box.get(),
                      'oid': id_entry_box.get(),
                  })

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

        # Grab the record number
        selected = database_tree.focus()
        # Update record
        database_tree.item(selected, text="", values=(
            id_entry_box.get(), name_entry_box.get(), stock_entry_box.get(), price_entry_box.get(),))

        # Clear entry boxes
        id_entry_box.delete(0, END)
        name_entry_box.delete(0, END)
        stock_entry_box.delete(0, END)
        price_entry_box.delete(0, END)
        database_tree.delete(*database_tree.get_children())

        # Run to pull data from database on start
        query_database()
    except Exception:
        print("exception")


# add new record to database
def add_record():
    global item_id
    # Update the database
    # Create a database or connect to one that exists
    conn = sqlite3.connect('pharmacy.db')

    # Create a cursor instance
    c = conn.cursor()
    if name_entry_box.get() == "":
        messagebox.showinfo('Input Error', 'No name')
        return
    elif stock_entry_box.get() == "":
        messagebox.showinfo('Input Error', 'No stock')
        return
    elif price_entry_box.get() == "":
        messagebox.showinfo('Input Error', 'No price')
        return

    # Add New Record
    try:
        c.execute("INSERT INTO medicine VALUES (:id, :name, :stock, :price)",
                  {
                      'id': item_id[-1] + 1,
                      'name': name_entry_box.get(),
                      'stock': stock_entry_box.get(),
                      'price': price_entry_box.get(),

                  })

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()
    except Exception:
        messagebox.showinfo('Database Error', 'Item name already exists')

    # Clear entry boxes
    id_entry_box.delete(0, END)
    name_entry_box.delete(0, END)
    stock_entry_box.delete(0, END)
    price_entry_box.delete(0, END)

    # Clear The Treeview Table
    database_tree.delete(*database_tree.get_children())

    # Run to pull data from database on start
    query_database()

#  -------------------------------------------------</Database Treeview functions>--------------------------------------
#  -------------------------------------------------<Data_frame Widgets>------------------------------------------------

# Add Record Entry Boxes


id_label = Label(data_frame, text="ID  : ")
id_label.grid(row=0, column=0, padx=10, pady=10)
id_label.configure(background=background_color)

id_entry_box = Entry(data_frame)
id_entry_box.grid(row=0, column=1, padx=10, pady=10)

name_label = Label(data_frame, text="Medicine Name  : ")
name_label.grid(row=0, column=2, padx=10, pady=10)
name_label.configure(background=background_color)

name_entry_box = Entry(data_frame)
name_entry_box.grid(row=0, column=3, padx=10, pady=10)

stock_label = Label(data_frame, text="Medicine Stock  : ")
stock_label.grid(row=1, column=0, padx=10, pady=10)
stock_label.configure(background=background_color)

stock_entry_box = Entry(data_frame)
stock_entry_box.grid(row=1, column=1, padx=10, pady=10)

price_label = Label(data_frame, text="Medicine Price  : ")
price_label.grid(row=1, column=2, padx=10, pady=10)
price_label.configure(background=background_color)

price_entry_box = Entry(data_frame)
price_entry_box.grid(row=1, column=3, padx=10, pady=10)

#  -------------------------------------------------</Data_frame Widgets>-----------------------------------------------
#  -------------------------------------------------<Button_frame Widgets>----------------------------------------------

# Add Buttons

update_button = Button(button_frame, text="Update Record", command=update_record)
update_button.grid(row=0, column=0, padx=10, pady=10)

add_button = Button(button_frame, text="Add Record", command=add_record)
add_button.grid(row=0, column=1, padx=10, pady=10)

remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
remove_one_button.grid(row=0, column=3, padx=10, pady=10)

select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
select_record_button.grid(row=0, column=7, padx=10, pady=10)
#  -------------------------------------------------</Button_frame Widgets>---------------------------------------------
#  -------------------------------------------------<Database_tree PS>--------------------------------------------------
# Bind the treeview
database_tree.bind("<ButtonRelease-1>", select_record)

query_database()
#  -------------------------------------------------</Database_tree PS>-------------------------------------------------
#  -------------------------------------------------<Search_frame Functions>--------------------------------------------


def search_now():
    id_entry_box.delete(0, END)
    name_entry_box.delete(0, END)
    stock_entry_box.delete(0, END)
    price_entry_box.delete(0, END)
    global Label1
    Label1 = Label(search_frame, text='          ').grid(row=1, column=0)
    searched_item = search_box.get()
    if searched_item == '':
        messagebox.showinfo("Type Error", "You haven't Entered the search parameter")
        return
    search_box.delete(0, END)
    print(searched_item)

    conn = sqlite3.connect('pharmacy.db')

    # Create a cursor instance
    c = conn.cursor()

    # Add New Record
    c.execute(f"SELECT * FROM medicine WHERE medicine_name LIKE '{searched_item}%' ")
    record = c.fetchall()

    Label1 = Label(search_frame, text=record).grid(row=1, column=0)
    print(record)
    try:
        id_entry_box.insert(0, record[0][0])
        name_entry_box.insert(0, record[0][1])
        stock_entry_box.insert(0, record[0][2])
        price_entry_box.insert(0, record[0][3])
    except Exception:
        messagebox.showinfo("Database Error", "No such item found in Database")
        return

    # Close our connection
    conn.close()

    return
#  -------------------------------------------------</Search_frame Functions>-------------------------------------------
#  -------------------------------------------------<Search_frame Widgets>----------------------------------------------


search_label = Label(search_frame, text='Search item  : ')
search_label.grid(row=0, column=0, padx=20, pady=20)
search_label.config(background=background_color)
search_box = Entry(search_frame)
search_box.grid(row=0, column=1, padx=20, pady=20)
Label1 = Label(search_frame, text='')
Label1.grid(row=1, column=0)
Label1.config(background=background_color)
search_button = Button(search_frame, text='Search Now', command=search_now)
search_button.grid(row=0, column=3, pady=20, padx=20)
#  -------------------------------------------------</Search_frame Widgets>---------------------------------------------
#  -------------------------------------------------<Account Tree view Options>-----------------------------------------
# Create a Treeview Frame

# Create a Treeview Scrollbar
account_tree_scroll = Scrollbar(account_tree_frame)
account_tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
account_tree = ttk.Treeview(account_tree_frame, yscrollcommand=account_tree_scroll.set, selectmode="extended")
account_tree.pack()

# Configure the Scrollbar
account_tree_scroll.config(command=account_tree.yview)

# Define Our Columns
account_tree['columns'] = ("ID", "Medicine Name", "Medicine Count", "Medicine Price")

# Format Our Columns
account_tree.column("#0", width=0, stretch=NO)
account_tree.column("ID", anchor=CENTER, width=100)
account_tree.column("Medicine Name", anchor=W, width=140)
account_tree.column("Medicine Count", anchor=CENTER, width=140)
account_tree.column("Medicine Price", anchor=W, width=140)

# Create Headings
account_tree.heading("#0", text="", anchor=W)
account_tree.heading("ID", text="ID", anchor=W)
account_tree.heading("Medicine Name", text="Medicine Name", anchor=W)
account_tree.heading("Medicine Count", text="Medicine Count", anchor=CENTER)
account_tree.heading("Medicine Price", text="Medicine Price", anchor=CENTER)

# Create Striped Row Tags
account_tree.tag_configure('oddrow', background="white")
account_tree.tag_configure('evenrow', background="lightblue")

basket_id_count = []
#  -------------------------------------------------</Account Tree view Options>----------------------------------------
#  -------------------------------------------------<Account Tree view Functions>---------------------------------------


def query_account_database():

    for i in range(len(basket_id_count)):
        if i % 2 == 0:
            account_tree.insert(parent='', index='end', iid=i, text='',
                                values=(basket_id_count[i][0], basket_id_count[i][1], basket_id_count[i][2],
                                        basket_id_count[i][3]),
                                tags=('evenrow',))
        else:
            account_tree.insert(parent='', index='end', iid=i, text='',
                                values=(basket_id_count[i][0], basket_id_count[i][1], basket_id_count[i][2],
                                        basket_id_count[i][3]),
                                tags=('oddrow',))


def account_search_now(event):
    global Label2
    Label2 = Label(account_search_frame, text='                                                ')
    Label2.grid(row=3, column=0)
    Label2.configure(background=background_color)
    searched_item = account_search_box.get()
    if searched_item == '':
        messagebox.showinfo("Type Error", "You haven't Entered the search parameter")
        return
    account_search_box.delete(0, END)

    conn = sqlite3.connect('pharmacy.db')

    # Create a cursor instance
    c = conn.cursor()

    # Add New Record
    c.execute(f"SELECT * FROM medicine WHERE medicine_name LIKE '{searched_item}%' ")
    records = c.fetchall()

    Label2 = Label(account_search_frame, text=records).grid(row=3, column=0)

    medicine_count = account_count_box.get()
    account_count_box.delete(0, END)
    if medicine_count == '':
        medicine_count = 1
    else:
        try:
            medicine_count = int(medicine_count)
        except Exception as e:
            messagebox.showinfo("Type Error", "Please Enter a valid number")
            print(e)
            return
    try:
        if int(records[0][2]) < medicine_count:
            messagebox.showinfo("Overflow Error", f"You only have >>{records[0][2]}<< of {records[0][1]}!")
            return
    except Exception:
        messagebox.showinfo("Database Error", "No such item found in Database")
        return

    basket_id_count.append([int(records[0][0]), records[0][1], medicine_count, records[0][3]])

    account_tree.delete(*account_tree.get_children())

    query_account_database()

    conn.close()
    return


def account_remove_one():
    x = account_tree.selection()[0]
    account_tree.delete(x)
    basket_id_count.pop(int(x))
#  -------------------------------------------------</Account Tree view Functions>--------------------------------------
#  -------------------------------------------------<Account_search_frame Widgets>--------------------------------------


account_search_label = Label(account_search_frame, text='Search  : ')
account_search_label.grid(row=0, column=0, padx=20, pady=20)
account_search_label.configure(background=background_color)

account_search_box = Entry(account_search_frame)
account_search_box.grid(row=0, column=1, padx=20, pady=20)

account_count_label = Label(account_search_frame, text='Count  : ')
account_count_label.grid(row=1, column=0, padx=20, pady=20)
account_count_label.configure(background=background_color)

account_count_box = Entry(account_search_frame)
account_count_box.grid(row=1, column=1, padx=20, pady=20)

Label2 = Label(account_search_frame, text='')
Label2.grid(row=3, column=0)
Label2.configure(background=background_color)

account_patient_fee_label = Label(account_search_frame, text="Patient Fee  : ")
account_patient_fee_label.grid(row=0, column=2, padx=20, pady=20)
account_patient_fee_label.configure(background=background_color)

account_patient_fee_box = Entry(account_search_frame)
account_patient_fee_box.grid(row=0, column=3, padx=20, pady=20)

#  -------------------------------------------------</Account_search_frame Widgets>-------------------------------------
#  -------------------------------------------------<Account_Options_frame Functions>-----------------------------------


def account_account_now():
    try:
        fee = int(account_patient_fee_box.get())
    except Exception:
        messagebox.showinfo('Invalid Input', 'Please enter patient fee/Proper Integer')
        return
    account_search_box.config(state='disabled')
    account_count_box.config(state='disabled')
    #    account_search_button.config(state='disabled')
    account_remove_one_button.config(state='disabled')
    account_patient_fee_box.config(state='disabled')
    #  -------------------------------------------------<Accounting_window>---------------------------------------------

    accounting_window = Tk()

    #  -------------------------------------------------</Accounting_window>--------------------------------------------
    #  -------------------------------------------------<Accounting_window_frames>--------------------------------------
    accounting_tree_frame = Frame(accounting_window)
    accounting_tree_frame.grid(row=0, column=1, padx=20)

    accounting_details_frame = LabelFrame(accounting_window, text='Accounting Details')
    accounting_details_frame.grid(row=0, column=0, padx=20)

    accounting_prices_frame = LabelFrame(accounting_window, text='Accounting Specifics')
    accounting_prices_frame.grid(row=1, column=0, padx=20)

    #  -------------------------------------------------</Accounting_window_frames>-------------------------------------
    #  -------------------------------------------------<Accounting_tree_options>---------------------------------------
    # Scroll Options
    accounting_tree_scroll = Scrollbar(accounting_tree_frame)
    accounting_tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    accounting_tree = ttk.Treeview(accounting_tree_frame, yscrollcommand=accounting_tree_scroll.set,
                                   selectmode="extended")
    accounting_tree.pack()

    # Configure the Scrollbar
    accounting_tree_scroll.config(command=accounting_tree.yview)

    # Define Our Columns
    accounting_tree['columns'] = ("ID", "Medicine Name", "Medicine Count", '*', "Medicine Price", 'Calculated Price')

    # Format Our Columns
    accounting_tree.column("#0", width=0, stretch=NO)
    accounting_tree.column("ID", anchor=CENTER, width=100)
    accounting_tree.column("Medicine Name", anchor=W, width=140)
    accounting_tree.column("Medicine Count", anchor=CENTER, width=140)
    accounting_tree.column("*", anchor=W, width=140)
    accounting_tree.column("Medicine Price", anchor=W, width=140)
    accounting_tree.column("Calculated Price", anchor=W, width=140)

    # Create Headings
    accounting_tree.heading("#0", text="", anchor=W)
    accounting_tree.heading("ID", text="ID", anchor=W)
    accounting_tree.heading("Medicine Name", text="Medicine Name", anchor=W)
    accounting_tree.heading("Medicine Count", text="Medicine Count", anchor=CENTER)
    accounting_tree.heading("*", text="*", anchor=CENTER)
    accounting_tree.heading("Medicine Price", text="Medicine Price", anchor=CENTER)
    accounting_tree.heading("Calculated Price", text="Calculated Price", anchor=CENTER)

    #  -------------------------------------------------</Accounting_tree_options>--------------------------------------
    #  -------------------------------------------------<Accounting_tree_functions>-------------------------------------
    unique_id = []
    unique_name = []
    unique_count = []
    unique_price = []
    unique_calc_price = []
    for x in basket_id_count:
        if x[0] not in unique_id:
            unique_id.append(x[0])

    for x in unique_id:
        sum = 0
        for i in range(len(basket_id_count)):
            if x == basket_id_count[i][0]:
                sum = sum + basket_id_count[i][2]
        unique_count.append(sum)

    conn = sqlite3.connect('pharmacy.db')

    c = conn.cursor()

    for x in unique_id:
        c.execute(f"SELECT * FROM medicine WHERE medicine_id = {x}")
        records = c.fetchall()
        for record in records:
            unique_name.append(record[1])
            unique_price.append(record[3])
            for i in range(len(unique_count)):
                if unique_count[i] > record[2]:
                    messagebox.showinfo("Database Error", f"You only have {record[2]} of {record[1]}")
                    accounting_window.destroy()
                    account_remove_one_button.config(state='normal')
                    account_search_box.config(state='normal')
                    account_count_box.config(state='normal')
                    account_patient_fee_box.config(state='normal')
                    return

    for i in range(len(unique_id)):
        unique_calc_price.append(unique_count[i] * unique_price[i])

    conn.close()
    new_table_data = []

    for i in range(len(unique_id)):
        new_table_data.append([unique_id[i], unique_name[i], unique_count[i], unique_price[i], unique_calc_price[i]])

    for i in range(len(new_table_data)):
        accounting_tree.insert(parent='', index='end', iid=i, text='',
                               values=(unique_id[i], unique_name[i], unique_count[i], "*", unique_price[i],
                                       unique_calc_price[i]),
                               tags=('evenrow',))

    def go_back():
        account_search_box.config(state='normal')
        account_count_box.config(state='normal')
        #        account_search_button.config(state='normal')
        account_remove_one_button.config(state='normal')
        account_patient_fee_box.config(state='normal')
        accounting_window.destroy()

    def commit_now():
        patient_name = accounting_patient_name_box.get()
        accounting_patient_name_box.delete(0, END)
        conn = sqlite3.connect('pharmacy.db')

        c = conn.cursor()
        for i in range(len(unique_id)):
            c.execute(f'SELECT * FROM medicine WHERE medicine_id = {unique_id[i]}')
            record = c.fetchall()
            count = record[0][2]
            rem = count - unique_count[i]
            c.execute(f"UPDATE medicine SET medicine_stock = {rem} WHERE medicine_id = {unique_id[i]}")

        conn.commit()
        conn.close()
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        current_time2 = now.strftime("%d/%m/%Y")
        count_str = ""
        name_str = ""
        print(unique_count)
        count_per_transaction = 0
        for count in unique_count:
            count_per_transaction = count_per_transaction + count

        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        sql = "INSERT INTO count_per_transaction VALUES ( ? , ? )"
        val = (current_time2, count_per_transaction)
        cursor.execute(sql, val)
        conn.commit()
        conn.close()

        for num in unique_count:
            str_num = str(num)
            count_str = count_str + str_num + ","

        count_str = count_str[:-1]

        for item in unique_name:
            name_str = name_str + item + ','
        name_str = name_str[:-1]
        transaction_details.append([patient_name, current_time, name_str, count_str, total])
        print(transaction_details)
        transaction_commit()
        transaction_details.clear()

        database_tree.delete(*database_tree.get_children())
        account_tree.delete(*account_tree.get_children())
        accounting_tree.delete(*accounting_tree.get_children())
        query_database()
        basket_id_count.clear()
        unique_id.clear()
        unique_count.clear()
        unique_name.clear()
        unique_price.clear()
        unique_calc_price.clear()

        account_search_box.config(state='normal')
        account_count_box.config(state='normal')
        #        account_search_button.config(state='normal')
        account_remove_one_button.config(state='normal')
        account_patient_fee_box.config(state='normal')
        accounting_window.destroy()

    #  -------------------------------------------------</Accounting_tree_functions>------------------------------------
    #  -------------------------------------------------<Accounting_details_widgets>------------------------------------
    drops_total = 0
    for item in unique_calc_price:
        drops_total = drops_total + item

    total = drops_total + fee

    def cash_now(e):
        cash = accounting_detail_given_cash_box.get()
        accounting_detail_given_cash_box.delete(0, END)
        try:
            cash = int(cash)
        except Exception:
            messagebox.showinfo('Input Error', 'Enter an valid integer')
            return

        accounting_detail_balance_label = Label(accounting_details_frame,
                                                text=f'         Balance  : {total} - {cash} =      ')
        accounting_detail_balance_label.grid(row=2, column=0, padx=20, pady=20)

        accounting_detail_balance = Label(accounting_details_frame, text=f'      {total - cash}     ')
        accounting_detail_balance.grid(row=2, column=1, padx=20, pady=20)

    accounting_detail_given_cash_label = Label(accounting_details_frame, text="Cash Given  : ")
    accounting_detail_given_cash_label.grid(row=0, column=0, padx=20, pady=20)

    accounting_detail_given_cash_box = Entry(accounting_details_frame)
    accounting_detail_given_cash_box.grid(row=0, column=1, padx=20, pady=20)

    accounting_detail_given_cash_box.bind('<Return>', cash_now)

    accounting_detail_total_label = Label(accounting_details_frame, text='Total Price  : ')
    accounting_detail_total_label.grid(row=1, column=0, padx=20, pady=20)

    accounting_detail_total = Label(accounting_details_frame, text=total)
    accounting_detail_total.grid(row=1, column=1, padx=20, pady=20)

    accounting_detail_balance_label = Label(accounting_details_frame, text=f'Balance  : {total} - Cash Given = ')
    accounting_detail_balance_label.grid(row=2, column=0, padx=20, pady=20)

    accounting_detail_balance = Label(accounting_details_frame, text=" ")
    accounting_detail_balance.grid(row=2, column=1, padx=20, pady=20)

    accounting_patient_name_label = Label(accounting_details_frame, text="Patient Name: ")
    accounting_patient_name_label.grid(row=3, column=0, padx=20, pady=20)

    accounting_patient_name_box = Entry(accounting_details_frame)
    accounting_patient_name_box.grid(row=3, column=1, padx=20, pady=20)

    accounting_go_back_button = Button(accounting_details_frame, text='Go back', command=go_back)
    accounting_go_back_button.grid(row=4, column=0, padx=20, pady=20)

    accounting_commit_button = Button(accounting_details_frame, text='Commit now', command=commit_now)
    accounting_commit_button.grid(row=4, column=1, padx=20, pady=20)
    #  -------------------------------------------------<Accounting_details_widgets>------------------------------------
    #  -------------------------------------------------<Accounting_prices_widgets>-------------------------------------

    count_per_transaction = 0
    for count in unique_count:
        count_per_transaction = count_per_transaction + count

    accounting_detail_drops_count_label = Label(accounting_prices_frame,
                                                text=f'No of drops: {count_per_transaction}')
    accounting_detail_drops_count_label.grid(row=0, column=0, padx=20, pady=20)

    accounting_detail_drops_total_label = Label(accounting_prices_frame, text=f'Drops Total: {drops_total}')
    accounting_detail_drops_total_label.grid(row=1, column=0, padx=20, pady=20)

    accounting_total_cost_label = Label(accounting_prices_frame,
                                        text=f'Total price (Drops + Fee) : {drops_total} + {fee} = {drops_total + fee}')
    accounting_total_cost_label.grid(row=2, column=0, padx=20, pady=20)

    accounting_total_change_500_label = Label(accounting_prices_frame, text=f'500 : {500 - total} ')
    accounting_total_change_500_label.grid(row=3, column=0, padx=20)
    accounting_total_change_500_label.config(background='yellow')

    accounting_total_change_1000_label = Label(accounting_prices_frame, text=f'1000 :  {1000 - total} ')
    accounting_total_change_1000_label.grid(row=4, column=0, padx=20)
    accounting_total_change_1000_label.config(background='red')

    accounting_total_change_1500_label = Label(accounting_prices_frame, text=f'1500 :  {1500 - total}')
    accounting_total_change_1500_label.grid(row=5, column=0, padx=20)
    accounting_total_change_1500_label.config(background='yellow')

    accounting_total_change_2000_label = Label(accounting_prices_frame, text=f'2000 :  {2000 - total}')
    accounting_total_change_2000_label.grid(row=6, column=0, padx=20)
    accounting_total_change_2000_label.config(background='red')

    accounting_total_change_2500_label = Label(accounting_prices_frame, text=f'2500 :  {2500 - total}')
    accounting_total_change_2500_label.grid(row=7, column=0, padx=20)
    accounting_total_change_2500_label.config(background='yellow')
    #  -------------------------------------------------</Accounting_prices_widgets>------------------------------------
    accounting_window.mainloop()
    #  -------------------------------------------------</Accounting Window>--------------------------------------------

#  -------------------------------------------------</Account Option frame Functions>-----------------------------------
#  -------------------------------------------------<Account Option frame Widgets>--------------------------------------


account_search_box.bind('<Return>', account_search_now)
account_count_box.bind('<Return>', account_search_now)

account_remove_one_button = Button(account_options_frame, text='Remove One', command=account_remove_one)
account_remove_one_button.grid(row=0, column=0, padx=20, pady=20)

account_account_now_button = Button(account_options_frame, text='Account Now', command=account_account_now)
account_account_now_button.grid(row=0, column=1, padx=20, pady=20)
query_account_database()
#  -------------------------------------------------</Account Option frame Widgets>-------------------------------------
#  -------------------------------------------------<Transaction Register Frame Functions>------------------------------


def transaction_register():
    #  -------------------------------------------------<Transaction Register Window>-----------------------------------
    transaction_register_window = Tk()
    transaction_register_window.title('Transaction Register')
    transaction_register_window.configure(background=background_color)
    #  -------------------------------------------------</Transaction Register Window>----------------------------------
    #  -------------------------------------------------<Transaction Register Frames>-----------------------------------
    daily_transaction_tree_frame = Frame(transaction_register_window)
    daily_transaction_tree_frame.grid(row=0, column=0, padx=20, pady=20)

    daily_tree_frame = Frame(transaction_register_window)
    daily_tree_frame.grid(row=0, column=1, padx=20, pady=20)

    monthly_tree_frame = Frame(transaction_register_window)
    monthly_tree_frame.grid(row=1, column=0, padx=20, pady=20)

    yearly_tree_frame = Frame(transaction_register_window)
    yearly_tree_frame.grid(row=1, column=1, padx=20, pady=20)

    all_transaction_tree_frame = Frame(transaction_register_window)
    all_transaction_tree_frame.grid(row=0, column=2, padx=20, pady=20)

    medicine_database_view_tree_frame = Frame(transaction_register_window)
    medicine_database_view_tree_frame.grid(row=1, column=2, padx=20, pady=20)

    button_frame = LabelFrame(transaction_register_window)
    button_frame.grid(row=2, column=0, padx=20, pady=20)
    button_frame.configure(background=background_color)
    #  -------------------------------------------------</Transaction Register Frames>----------------------------------
    #  -------------------------------------------------<Daily Transaction Tree options>--------------------------------

    # Create The Treeview
    daily_transaction_tree_scroll = Scrollbar(daily_transaction_tree_frame)
    daily_transaction_tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    daily_transaction_tree = ttk.Treeview(daily_transaction_tree_frame,
                                          yscrollcommand=daily_transaction_tree_scroll.set, selectmode="extended")
    daily_transaction_tree.pack()

    # Configure the Scrollbar
    daily_transaction_tree_scroll.config(command=daily_transaction_tree.yview)

    # Define Our Columns
    daily_transaction_tree['columns'] = ("Daily Transaction Date", "Counting")

    # Format Our Columns
    daily_transaction_tree.column("#0", width=0, stretch=NO)
    daily_transaction_tree.column("Daily Transaction Date", anchor=CENTER, width=200)
    daily_transaction_tree.column("Counting", anchor=W, width=140)

    # Create Headings
    daily_transaction_tree.heading("#0", text="", anchor=W)
    daily_transaction_tree.heading("Daily Transaction Date", text="Daily Transaction Date", anchor=W)
    daily_transaction_tree.heading("Counting", text="Counting", anchor=W)
    # Create Striped Row Tags
    daily_transaction_tree.tag_configure('oddrow', background="white")
    daily_transaction_tree.tag_configure('evenrow', background="lightblue")
    #  -------------------------------------------------</Daily Transaction Tree options>-------------------------------
    #  -------------------------------------------------<Daily  Tree options>-------------------------------------------
    daily_tree_scroll = Scrollbar(daily_tree_frame)
    daily_tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    daily_tree = ttk.Treeview(daily_tree_frame, yscrollcommand=daily_tree_scroll.set, selectmode="extended")
    daily_tree.pack()

    # Configure the Scrollbar
    daily_tree_scroll.config(command=daily_tree.yview)

    # Define Our Columns
    daily_tree['columns'] = ("Daily Date", "Count")

    # Format Our Columns
    daily_tree.column("#0", width=0, stretch=NO)
    daily_tree.column("Daily Date", anchor=CENTER, width=200)
    daily_tree.column("Count", anchor=W, width=140)

    # Create Headings
    daily_tree.heading("#0", text="", anchor=W)
    daily_tree.heading("Daily Date", text="Daily Date", anchor=W)
    daily_tree.heading("Count", text="Count per Day", anchor=W)

    # Create Striped Row Tags
    daily_tree.tag_configure('oddrow', background="white")
    daily_tree.tag_configure('evenrow', background="lightblue")
    #  -------------------------------------------------</Daily  Tree options>------------------------------------------
    #  -------------------------------------------------<Monthly  Tree options>-----------------------------------------
    monthly_tree_scroll = Scrollbar(yearly_tree_frame)
    monthly_tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    monthly_tree = ttk.Treeview(monthly_tree_frame, yscrollcommand=monthly_tree_scroll.set, selectmode="extended")
    monthly_tree.pack()

    # Configure the Scrollbar
    monthly_tree_scroll.config(command=monthly_tree.yview)

    # Define Our Columns
    monthly_tree['columns'] = ("Monthly Date", "Count")

    # Format Our Columns
    monthly_tree.column("#0", width=0, stretch=NO)
    monthly_tree.column("Monthly Date", anchor=CENTER, width=200)
    monthly_tree.column("Count", anchor=W, width=140)

    # Create Headings
    monthly_tree.heading("#0", text="", anchor=W)
    monthly_tree.heading("Monthly Date", text="Monthly Date", anchor=W)
    monthly_tree.heading("Count", text="Count per month", anchor=W)

    # Create Striped Row Tags
    monthly_tree.tag_configure('oddrow', background="white")
    monthly_tree.tag_configure('evenrow', background="lightblue")

    #  -------------------------------------------------</Monthly  Tree options>----------------------------------------
    #  -------------------------------------------------<Yearly  Tree options>------------------------------------------
    yearly_tree_scroll = Scrollbar(yearly_tree_frame)
    yearly_tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    yearly_tree = ttk.Treeview(yearly_tree_frame, yscrollcommand=yearly_tree_scroll.set, selectmode="extended")
    yearly_tree.pack()

    # Configure the Scrollbar
    yearly_tree_scroll.config(command=yearly_tree.yview)

    # Define Our Columns
    yearly_tree['columns'] = ("Year Date", "Count")

    # Format Our Columns
    yearly_tree.column("#0", width=0, stretch=NO)
    yearly_tree.column("Year Date", anchor=CENTER, width=200)
    yearly_tree.column("Count", anchor=W, width=140)

    # Create Headings
    yearly_tree.heading("#0", text="", anchor=W)
    yearly_tree.heading("Year Date", text="Year Date", anchor=W)
    yearly_tree.heading("Count", text="Count per Year", anchor=W)

    # Create Striped Row Tags
    yearly_tree.tag_configure('oddrow', background="white")
    yearly_tree.tag_configure('evenrow', background="lightblue")

    #  -------------------------------------------------</Yearly  Tree options>-----------------------------------------
    #  -------------------------------------------------<All Transaction Tree options>----------------------------------
    all_transaction_tree_scroll = Scrollbar(all_transaction_tree_frame)
    all_transaction_tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    all_transaction_tree = ttk.Treeview(all_transaction_tree_frame, yscrollcommand=all_transaction_tree_scroll.set,
                                        selectmode="extended")
    all_transaction_tree.pack()

    # Configure the Scrollbar
    all_transaction_tree_scroll.config(command=all_transaction_tree.yview)

    # Define Our Columns
    all_transaction_tree['columns'] = (
        "Patient Name", "Date of Transaction", "Item Names", "Item Counts", "Total Price")

    # Format Our Columns
    all_transaction_tree.column("#0", width=0, stretch=NO)
    all_transaction_tree.column("Patient Name", anchor=CENTER, width=200)
    all_transaction_tree.column("Date of Transaction", anchor=W, width=140)
    all_transaction_tree.column("Item Names", anchor=W, width=140)
    all_transaction_tree.column("Item Counts", anchor=W, width=140)
    all_transaction_tree.column("Total Price", anchor=W, width=140)

    # Create Headings
    all_transaction_tree.heading("#0", text="", anchor=W)
    all_transaction_tree.heading("Patient Name", text="Patient Name", anchor=W)
    all_transaction_tree.heading("Date of Transaction", text="Date of Transaction", anchor=W)
    all_transaction_tree.heading("Item Names", text="Item Names", anchor=W)
    all_transaction_tree.heading("Item Counts", text="Item Counts", anchor=W)
    all_transaction_tree.heading("Total Price", text="Total Price", anchor=W)

    # Create Striped Row Tags
    all_transaction_tree.tag_configure('oddrow', background="white")
    all_transaction_tree.tag_configure('evenrow', background="lightblue")
    #  -------------------------------------------------</All Transaction Tree options>---------------------------------
    #  -------------------------------------------------<Medicine Database View Tree options>---------------------------

    medicine_database_view_tree_scroll = Scrollbar(medicine_database_view_tree_frame)
    medicine_database_view_tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    medicine_database_view_tree = ttk.Treeview(medicine_database_view_tree_frame,
                                               yscrollcommand=medicine_database_view_tree_scroll.set,
                                               selectmode="extended")
    medicine_database_view_tree.pack()

    # Configure the Scrollbar
    medicine_database_view_tree_scroll.config(command=all_transaction_tree.yview)

    # Define Our Columns
    medicine_database_view_tree['columns'] = (
        "ID", "Medicine Name", "Item Count", "Item Price")

    # Format Our Columns
    medicine_database_view_tree.column("#0", width=0, stretch=NO)
    medicine_database_view_tree.column("ID", anchor=CENTER, width=200)
    medicine_database_view_tree.column("Medicine Name", anchor=W, width=140)
    medicine_database_view_tree.column("Item Count", anchor=W, width=140)
    medicine_database_view_tree.column("Item Price", anchor=W, width=140)

    # Create Headings
    medicine_database_view_tree.heading("#0", text="", anchor=W)
    medicine_database_view_tree.heading("ID", text="ID", anchor=W)
    medicine_database_view_tree.heading("Medicine Name", text="Medicine Name", anchor=W)
    medicine_database_view_tree.heading("Item Count", text="Item Count", anchor=W)
    medicine_database_view_tree.heading("Item Price", text="Item Price", anchor=W)

    # Create Striped Row Tags
    medicine_database_view_tree.tag_configure('oddrow', background="white")
    medicine_database_view_tree.tag_configure('evenrow', background="lightblue")

    #  -------------------------------------------------<Medicine Database View Tree options>---------------------------
    #  -------------------------------------------------<Transaction Register Functions>--------------------------------
    def create_count_sql():

        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE if not exists count_per_transaction(                        
            time text,
            daily_transaction_counts text)""")
        # creates the databases..daily_count and monthly_count
        cursor.execute("""CREATE TABLE if not exists daily_count(                        
        time text,
        daily_counts text)""")

        cursor.execute("""CREATE TABLE if not exists monthly_count(
        time text,
        monthly_counts text)""")

        cursor.execute("""CREATE TABLE if not exists yearly_count(
        time text,
        yearly_counts text)""")
        conn.commit()
        conn.close()

    def counting_function_sql():
        #  -------------------------------------------------<Medicine Database View tree Function>----------------------
        selected_asc_desc = drop_box_asc_desc.get()
        if selected_asc_desc == "Ascending":
            selected_1 = 'ASC'
        elif selected_asc_desc == "Descending":
            selected_1 = 'DESC'
        selected_name_count_price = drop_box_name_count_price.get()
        if selected_name_count_price == "Name":
            selected_2 = "medicine_name"
        elif selected_name_count_price == "Count":
            selected_2 = "medicine_stock"
        elif selected_name_count_price == "Price":
            selected_2 = "medicine_price"

        conn = sqlite3.connect('pharmacy.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM medicine ORDER BY {selected_2} {selected_1}")
        recordk = c.fetchall()
        for i in range(len(recordk)):
            if i % 2 == 0:
                medicine_database_view_tree.insert(parent='', index='end', iid=i, text='',
                                                   values=(recordk[i][0], recordk[i][1], recordk[i][2], recordk[i][3]),
                                                   tags=('evenrow',))

            else:
                medicine_database_view_tree.insert(parent='', index='end', iid=i, text='',
                                                   values=(recordk[i][0], recordk[i][1], recordk[i][2], recordk[i][3]),
                                                   tags=('oddrow',))
        #  -------------------------------------------------</Medicine Database View tree Function>---------------------
        #  -------------------------------------------------<All Transaction tree Function>-----------------------------
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        record0 = cursor.fetchall()
        list0 = []
        for i in range(len(record0)):
            list0.append([record0[i][0], record0[i][1]])
            if i % 2 == 0:
                all_transaction_tree.insert(parent='', index='end', iid=i, text='',
                                            values=(
                                                record0[i][0], record0[i][1], record0[i][2], record0[i][3],
                                                record0[i][4]),
                                            tags=('evenrow',))

            else:
                all_transaction_tree.insert(parent='', index='end', iid=i, text='',
                                            values=(
                                                record0[i][0], record0[i][1], record0[i][2], record0[i][3],
                                                record0[i][4]),
                                            tags=('oddrow',))

        headers = ('Patient Name', 'Date of Transaction', 'Item Names', 'Item Counts', 'Total Price')
        table1 = tabulate(list0, headers, tablefmt="grid")
        print(table1)
        #  -------------------------------------------------</All Transaction tree Function>----------------------------
        #  -------------------------------------------------<Count per Transaction tree Function>-----------------------
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM count_per_transaction")
        record1 = cursor.fetchall()
        list1 = []
        for i in range(len(record1)):
            list1.append([record1[i][0], record1[i][1]])
            if i % 2 == 0:
                daily_transaction_tree.insert(parent='', index='end', iid=i, text='',
                                              values=(record1[i][0], record1[i][1]), tags=('evenrow',))

            else:
                daily_transaction_tree.insert(parent='', index='end', iid=i, text='',
                                              values=(record1[i][0], record1[i][1]), tags=('oddrow',))

        headers = ('Date of transaction', 'Count')
        table1 = tabulate(list1, headers, tablefmt="grid")
        print(table1)

        unique_time = []
        daily_transaction_counts = []
        for x in record1:
            if x[0] not in unique_time:
                unique_time.append(x[0])
        print('Unique Time: ', unique_time)

        for date in unique_time:
            daily_transaction_count = 0
            for x in record1:
                if x[0] == date:
                    daily_transaction_count = daily_transaction_count + int(
                        x[1])  # Tuples (date , total count in that date )
            daily_transaction_counts.append(daily_transaction_count)
        #  -------------------------------------------------</Count per Transaction tree Function>----------------------
        #  -------------------------------------------------<Daily_count tree Function>--------------------------------
        print('Daily transaction counts : ', daily_transaction_counts)
        for i in range(len(unique_time)):
            conn = sqlite3.connect('pharmacy.db')
            cursor = conn.cursor()
            sql = "INSERT INTO daily_count VALUES ( ? , ? )"  # Tuples inserted into daily_count
            val = (unique_time[i], daily_transaction_counts[i])
            cursor.execute(sql, val)
            conn.commit()
            conn.close()

        conn.close()

        conn = sqlite3.connect('pharmacy.db')  # Shows values from daily count( date , total count in that date)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM daily_count")
        record2 = cursor.fetchall()
        list2 = []
        for i in range(len(record2)):
            list2.append([record2[i][0], record2[i][1]])
            if i % 2 == 0:
                daily_tree.insert(parent='', index='end', iid=i, text='', values=(record2[i][0], record2[i][1]),
                                  tags=('evenrow',))

            else:
                daily_tree.insert(parent='', index='end', iid=i, text='', values=(record2[i][0], record2[i][1]),
                                  tags=('oddrow',))

        headers = ('Date-Day of  transaction', 'Count')
        table2 = tabulate(list2, headers, tablefmt="grid")
        print(table2)

        unique_month_time = []
        unique_year_time = []
        monthly_counts = []
        for x in record1:
            if x[0][3:] not in unique_month_time:
                unique_month_time.append(x[0][3:])
            if x[0][6:] not in unique_year_time:
                unique_year_time.append(x[0][6:])

        for date in unique_month_time:
            monthly_count = 0
            for x in record1:  # Tuples (Month , Total count in that month) created
                if x[0][3:] == date:
                    monthly_count = monthly_count + int(x[1])
            monthly_counts.append(monthly_count)
        #  -------------------------------------------------</Daily count tree Function>--------------------------------
        #  -------------------------------------------------<Monthly tree Function>--------------------------------
        for i in range(len(unique_month_time)):
            conn = sqlite3.connect('pharmacy.db')
            cursor = conn.cursor()
            sql = "INSERT INTO monthly_count VALUES ( ? , ? )"  # Tuples added to monthly_count
            val = (unique_month_time[i], monthly_counts[i])
            cursor.execute(sql, val)
            conn.commit()
            conn.close()

        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM monthly_count")
        record3 = cursor.fetchall()
        list3 = []
        for i in range(len(record3)):
            list3.append([record3[i][0], record3[i][1]])
            if i % 2 == 0:
                monthly_tree.insert(parent='', index='end', iid=i, text='', values=(record3[i][0], record3[i][1]),
                                    tags=('evenrow',))

            else:
                monthly_tree.insert(parent='', index='end', iid=i, text='', values=(record3[i][0], record3[i][1]),
                                    tags=('oddrow',))

        headers = ('Month of Transaction', 'Count')
        table3 = tabulate(list3, headers, tablefmt="grid")
        print(table3)

        yearly_count = []
        for date in unique_year_time:
            year_count = 0
            for x in record1:  # Tuples (Month , Total count in that month) created
                if x[0][6:] == date:
                    year_count = year_count + int(x[1])
            yearly_count.append(year_count)
        #  -------------------------------------------------</Monthly tree Function>--------------------------------
        #  -------------------------------------------------<Yearly tree Function>--------------------------------
        for i in range(len(unique_year_time)):
            conn = sqlite3.connect('pharmacy.db')
            cursor = conn.cursor()
            sql = "INSERT INTO yearly_count VALUES ( ? , ? )"
            val = (unique_year_time[i], yearly_count[i])
            cursor.execute(sql, val)
            conn.commit()
            conn.close()

        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM yearly_count")
        record4 = cursor.fetchall()
        list4 = []
        for i in range(len(record4)):
            list4.append([record4[i][0], record4[i][1]])
            if i % 2 == 0:
                yearly_tree.insert(parent='', index='end', iid=i, text='', values=(record4[i][0], record4[i][1]),
                                   tags=('evenrow',))

            else:
                yearly_tree.insert(parent='', index='end', iid=i, text='', values=(record4[i][0], record4[i][1]),
                                   tags=('oddrow',))

        headers = ('Date of transaction', 'Count')
        table4 = tabulate(list4, headers, tablefmt="grid")
        print(table4)
        #  -------------------------------------------------</Monthly tree Function>--------------------------------
        #  -------------------------------------------------<Yearly tree Function>--------------------------------

    def delete_counting_function_sql():
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute("DROP TABLE daily_count")
        cursor.execute("DROP TABLE monthly_count")
        cursor.execute("DROP TABLE yearly_count")
        conn.commit()
        conn.close()
        return

    def refresh_now():
        medicine_database_view_tree.delete(*medicine_database_view_tree.get_children())
        all_transaction_tree.delete(*all_transaction_tree.get_children())
        daily_transaction_tree.delete(*daily_transaction_tree.get_children())
        daily_tree.delete(*daily_tree.get_children())
        monthly_tree.delete(*monthly_tree.get_children())
        yearly_tree.delete(*yearly_tree.get_children())
        create_count_sql()
        counting_function_sql()
        delete_counting_function_sql()

    #  -------------------------------------------------<Button Frame Widgets>------------------------------------------

    drop_box_asc_desc = ttk.Combobox(button_frame, state="readonly", value=["Ascending", "Descending"])
    drop_box_asc_desc.current(0)
    drop_box_asc_desc.grid(row=2, column=0)
    drop_box_name_count_price = ttk.Combobox(button_frame, state="readonly", value=["Name", "Count", "Price"])
    drop_box_name_count_price.current(1)
    drop_box_name_count_price.grid(row=1, column=0)
    create_count_sql()
    counting_function_sql()
    delete_counting_function_sql()

    refresh_now_button = Button(button_frame, text='Refresh Now', command=refresh_now)
    refresh_now_button.grid(row=0, column=0, padx=20, pady=20)
    #  -------------------------------------------------<Button Frame Widgets>------------------------------------------
    transaction_register_window.mainloop()
#  -------------------------------------------------</Transaction Register Frame Functions>-----------------------------
#  -------------------------------------------------<Transaction Register Frame Widgets>--------------------------------


transaction_register_button = Button(transaction_register_frame, text='Open Transaction Register',
                                     command=transaction_register)
transaction_register_button.grid(row=0, column=0, padx=20, pady=20)
#  -------------------------------------------------</Transaction Register Frame Widgets>-------------------------------
#  -------------------------------------------------</Main Window>------------------------------------------------------
root.mainloop()
