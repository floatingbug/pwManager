#!/usr/bin/env python3.8

import random
import string
import sqlite3
from sqlite3 import Error

def userInput():
    i = input(">>> ")
    
    return i

def showHelp():
    print("""
            to manage passwords it is neccessary to be logged in.
            
            example: c yahoo l=12 n=3 r
                -> creates a Password for yahoo with length=12, 
                    numbers=3, contains capital letters.

            h or --help -----> show commants
            q           -----> quit
            login       -----> log in
                                -> syntax: login <name>
            sign        -----> sign up
                                -> syntax: sign <name>
            who         -----> show current logged user
            c           -----> create new password
                                -> syntax: c <name> <password>
            l           -----> password create automatically (only small letters)
                                -> syntax: c yahoo l=8
            r           -----> crate random small and capital letters (l needed)
            n           -----> numbers of digits
            show <name> -----> show password of corresponding name
            show names  -----> show all names
            rm <name>   -----> remove name and corresponding password
            """)

def saveUserToDb(name, password):
    try:
        con = sqlite3.connect("../data/shadow.db")
        cur = con.cursor()

        cur.execute("INSERT INTO users VALUES(?, ?)", (name, password,))
        con.commit()

    except Error as e:
        print("DB Error: ", e)
    finally:
        con.close()

def save_account_to_db(username, accountname, password):
    try:
        con = sqlite3.connect("../data/account.db")
        cur = con.cursor()

        cur.execute("INSERT INTO account VALUES(?, ?, ?)", (username, accountname, password,))
        con.commit()
    except Error as e:
        print("DB Error: ", e)
    finally:
        con.close()

def sign():
    name = input("enter a name: ")
    
    if name == "":
        print("name is required")
        return "sign"
    
    print("""
        if u skip password by pressing enter, the account will created
        without a password.
    """)
    password = input("enter a password: ")
    if password == "":
        password = "none"

    try:
        con = sqlite3.connect("../data/shadow.db")
        cur = con.cursor()

        res = cur.execute("SELECT * FROM users WHERE name=?", (name,))
        res = res.fetchone()

        if res != None:
            print("name: ", name, ", allready in use")
        else:
            saveUserToDb(name, password)
            print("new account added")
            #if sign success go out of sign-function
            return "userInput"
        
        #if sign fail start sign-function again
        return "sign"
    
    except Error as e:
        print("DB Error: ", e)
    
    finally:
        con.close()

def login(user):
    print("login to account")
    name = input("name: ")
    
    try:
        con = sqlite3.connect("../data/shadow.db")
        cur = con.cursor()

        res = cur.execute("SELECT * FROM users WHERE name=?", (name,))
        res = res.fetchone()
        print(res)

    except Error as e:
        print("DB Error: ", e)
    finally:
        con.close()
    
    if res == None:
        print("name: ", name, " does not exist")
        return "login"
    if res[1] == "none":
        user.update({'name': name})
        print("login success")
        return "userInput"
    else:
        password = input("password: ")
        
        if res[1] != password:
            print("wrong password")
            return "userInput"
        else:
            user['name'] = name
            user['password'] = password
            print("login success")
            return "userInput"

def showCurrUser(user):
    print(user['name'])

def check_if_login(user):
    if user['name'] == "":
        return False
    else:
        return True

def random_pw(l, n, r):
    l = int(l)
    new_pw = ""
    
    #create random pw (letters only)
    for i in range(l):
        random_letter = random.choice(string.ascii_letters)
        new_pw = new_pw + random_letter
    
    #create random numbers
    if n >= l:
        print("n must be less then l")
        return "userInput"
    if n != "":
        n = int(n)
        exit = False
        counter = 0
        random_index = []
        
        while not exit:
            tmp_index = random.randrange(1, l)
            
            if tmp_index in random_index:
                continue
            else:
                random_index.append(tmp_index)
                counter = counter + 1
            if counter == n:
                exit = True
    
        for i in range(0, n):
            tmp_index = random_index[n]
            new_pw[tmp_intex] = int(random.random()*10)
    
    #make from random small letter in new_pw capital letters
    if r:
        exit = False
        counter = 0
        pw_in_array = []
        number_of_capital_letters = (l - int(n)) / 2

        for i in range(0, l):
            pw_in_array.append = new_pw[i]

        while not exit:
            tmp_index = random.randrange(0, l)

            if new_pw[tmp_index].isdigit() or new_pw[tmp_index].isupper():
                continue
            else:
                pw_in_array[tmp_index] = pw_in_array[tmp_index].upper()
                counter = counter + 1
            if number_of_capital_letters <= counter:
                exit = True

    return new_pw

def create_pw(v, user):
    pw = ""
    account = ""
    user_defined = False
    r = False
    n = ""
    l = ""
    args = v.split()
    
    #check for correct syntax
    if not check_if_login(user):
        print("please login first")
        return "userInput"
    
    if not "l=" in args[2]:
        user_defined = True
    if user_defined and args[1] == "" or args[2] == "":
        print("account and password is needed")
        return "userInput"
    if not user_defined:
        for arg in args:
            if 'l=' in arg:
                l = arg.strip("l=")
                if not l.isdigit():
                    print("argument: l, need to be a number")
                    return "userInput"
            if 'n=' in args:
                n = arg.strip("n=")
                if not n.isdigit():
                    print("argument: n, need to be a number")
                    return "userInput"
            if arg == "r":
                r = True
    
        #create pw automatically
        random_pw(l, n, r)
        print("account added to db")
        return "userInput"

    #crate userdefined pw (not automatic)
    if user_defined:
        account = args[1]
        pw = args[2]
        
        save_account_to_db(user['name'], account, pw)
        print("account added to db")
        return "userInput"
    
    #create automatically a pw
    random_pw(l, n, r)

def show_pw(v, user):
    args = v.split()
    res = []
    account = ""

    #check for correct syntax
    if not check_if_login(user):
        print("please login first")
        return "userInput"
    if args[1] != "name" and args[1] != "names":
        print("secont argument must be name or names")
        return "userInput"
    if args[1] == "name" and args[2] == "":
        print("third argument is needed")
        return "userInput"

    else:
        try:
            con = sqlite3.connect("../data/account.db")
            cur = con.cursor()

            res = cur.execute("SELECT account, password FROM account")
            res = res.fetchall()
        except Error as e:
            print("DB Error: ", e)
        finally:
            con.close()

    if args[1] == "names":
        for t in res:
            print("account: ", t[0], "----> password: ", t[1])

        return "userInput"
    else:
        account = args[2]

        for t in res:
            if t[0] == account:
                print("account: ", t[0], "----> password: ", t[1])
                break
        
        return "userInput"

    print("no account: ", account, ", found")
    return "userInput"

# Main-Function
def main():
    q = False
    user = {'name': "", 'password': ""}
    v = "userInput"

    while not q:
        if v == "userInput":
            v = userInput()
        elif v == "h" or v == "--help":
            showHelp()
            v = "userInput"
            continue
        elif v[0] == "c":
            v = create_pw(v, user)
            continue
        elif "show" in v:
            v = show_pw(v, user)
        elif v == "sign":
            v = sign()
        elif v == "login":
            v = login(user)
            print(user)
        elif v == "who":
            showCurrUser(user)
            v = "userInput"
            continue
        elif v == "q":
            q = True
        elif v != "sign" and v != "login":
            print("command: ", v, " not found")
            v = "userInput"

if __name__ == "__main__":
    main()
else:
    print("pwManager is the main program, don't use it as a module")



