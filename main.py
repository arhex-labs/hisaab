import sqlite3
import os.path
import time
import os
from datetime import date, datetime
import csv

def create_db():
    con = sqlite3.connect('hisaab.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE ledger (ledger_name TEXT, ledger_desc TEXT, ledger_date TEXT, ledger_dr INTEGER, ledger_cr INTEGER)")
    con.close()

def file_exist(filename):
    if os.path.isfile(filename):
        return True
    else:
        return False

def show_balance():
    rows = cur.execute("SELECT * FROM ledger").fetchall()
    dr = 0
    cr = 0
    for i in rows:
        dr = dr + i[3]
        cr = cr + i[4]
    return dr - cr

def show_ledger():
    rows = cur.execute("SELECT * FROM ledger").fetchall()
    for i in rows:
        datenow = str(i[2])
        datenow = datenow.split()
        datenow = datenow[0]
        with open('hisaab.csv', mode='a') as ledger:
            writer = csv.writer(ledger, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([i[0], i[1], datenow, i[3], i[4]])
    input('File Saved. Press enter to continue...')
    os.system('clear')

def show_banner():
    print('*************************')
    print('Hisaab Kitaab')
    print('Created By: ARHEX LABS')
    print('Version: 0.1')
    print('Balance: ', end="")
    print(show_balance())
    print('*************************')

def show_menu():
    print('1: Add Balance')
    print('2: Add Expense')
    print('3: Save Ledger')

def add_balance():
    name = input('Enter Name: ')
    desc = input('Enter Description: ')
    today = str(datetime.now())
    amount = int(input('Enter Ammount: '))
    query = "INSERT INTO ledger VALUES ('" + name + "', '" + desc + "', '" + today + "', '" + str(amount) + "', 0)"
    cur.execute(query)
    print('Amount Added. ' + str(con.total_changes) + " rows affected." )
    con.commit()
    time.sleep(1)
    os.system('clear')

def add_expense():
    name = input('Enter Name: ')
    desc = input('Enter Description: ')
    today = str(datetime.now())
    amount = int(input('Enter Ammount: '))
    query = "INSERT INTO ledger VALUES ('" + name + "', '" + desc + "', '" + today + "', 0, " + str(amount) + ")"
    cur.execute(query)
    print('Amount Added. ' + str(con.total_changes) + " rows affected." )
    con.commit()
    time.sleep(1)
    os.system('clear')

def main():
    show_banner()
    show_menu()

if __name__ == '__main__':
    if file_exist('hisaab.db'):
        print('Connecting to Database...')
        time.sleep(1)
        con = sqlite3.connect('hisaab.db')
        cur = con.cursor()
        print('Connected.')
        time.sleep(1)
        os.system('clear')
    else:
        print('Creating Database...')
        create_db()
        print('Database Created.')
        print('Connecting to Database...')
        time.sleep(1)
        con = sqlite3.connect('hisaab.db')
        cur = con.cursor()
        print('Connected.')
        time.sleep(1)
        os.system('clear')

    while True:
        main()
        choice = int(input("Your Choice => "))
        if choice == 1:
            add_balance()
        elif choice == 2:
            add_expense()
        elif choice == 3:
            show_ledger()
        else:
            print('Good Bye ;)')
            con.close()
            exit()