#!/usr/bin/env python3.8


import random
import string
import sqlite3
from sqlite3 import Error

def userInput():
    i = input(">>> ")
    v = i.split()

    return v

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
                                -> syntax: sign 
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

    return ["userInput"]

def saveUserToDb(name, password):
    success = False

    try:
        con = sqlite3.connect("../data/shadow.db")
        cur = con.cursor()

        cur.execute("INSERT INTO users VALUES(?, ?)", (name, password,))
        con.commit()
        success = True
    except Error as e:
        print("DB Error: ", e)
    finally:
        con.close()

    return success

def save_account_to_db(username, accountname, password):
    try:
        con = sqlite3.connect("../data/account.db")
        cur = con.cursor()

        cur.execute("INSERT INTO account VALUES(?, ?, ?)", (username, accountname, password,))
        con.commit()
        print("account added to db")
    except Error as e:
        print("DB Error: ", e)
    finally:
        con.close()

def sign():
    name = input("enter a name: ")
    
    if name == "":
        print("name is required")
        return ["sign"]
    
    print("""
        if u skip password by pressing enter, the account will created
        without a password.
    """)
    password = input("enter a password: ")
    if password == "":
        password = "none"
    
    name_allready_exists = False
    
    #check if name allready exists
    try:
        con = sqlite3.connect("../data/shadow.db")
        cur = con.cursor()

        res = cur.execute("SELECT * FROM users WHERE name=?", (name,))
        res = res.fetchone()
        
        if res != None:
            name_allready_exists = True
    
    except Error as e:
        print("DB Error: ", e)
    finally:
        con.close()
    
    #if user allready exists start sign-function again
    if name_allready_exists:
        print("name: ", name, ", allready in use")
        return ["sign"]
    
    #save new user to db
    success = saveUserToDb(name, password)
    if success:
        print("new user saved to db")
        return ["userInput"]
    else:
        print("something goes wrong :(")
        return ["userInput"]


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
        return ["login"]
    if res[1] == "none":
        user.update({'name': name})
        print("login success")
        return ["userInput"]
    else:
        password = input("password: ")
        
        if res[1] != password:
            print("wrong password")
            return ["userInput"]
        else:
            user['name'] = name
            user['password'] = password
            print("login success")
            return ["userInput"]

def showCurrUser(user):
    print(user['name'])
    
    return ["userInput"]

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
        random_letter = random.choice(string.ascii_lowercase)
        new_pw = new_pw + random_letter
    
    #create random numbers
    if n != "":
        
        n = int(n)
        exit = False
        counter = 0
        random_index = []
        
        if n >= l:
            print("n must be less then l")
            return ["userInput"]
        
        while not exit:
            tmp_index = random.randrange(0, l)
            
            if tmp_index in random_index:
                continue
            else:
                random_index.append(tmp_index)
                counter = counter + 1
            if counter == n:
                exit = True
    
        for i in range(len(random_index)):
            tmp_index = random_index[i]
            random_number = int(random.random()*10)
            random_number = str(random_number)

            new_pw = new_pw[0:tmp_index] + random_number + new_pw[tmp_index+1:len(new_pw)]
    
    #make from random small letter in new_pw capital letters
    if r:
        exit = False
        counter = 0
        number_of_capital_letters = (l - int(n)) / 2

        while not exit:
            tmp_index = random.randrange(0, l)

            if new_pw[tmp_index].isdigit() or new_pw[tmp_index].isupper():
                continue
            else:
                new_pw = new_pw[0:tmp_index] + new_pw[tmp_index:tmp_index+1].upper() + new_pw[tmp_index+1:len(new_pw)]
                counter = counter + 1
            if number_of_capital_letters <= counter:
                exit = True

    return new_pw

def create_pw(v, user):
    pw = ""
    user_defined = False
    r = False
    n = ""
    l = ""
    args = v
    
    #check for correct syntax
    if not check_if_login(user):
        print("please login first")
        return ["userInput"]
    if len(args) <= 2:
        print("need more arguments")
        return ["userInput"]
    
    #check if pw is user defined or not
    if not "l=" in args[2]:
        user_defined = True
    
    #set variables needed to automatically created pw and
    #create pw (if not user defined)
    if not user_defined:
        for arg in args:
            if 'l=' in arg:
                l = arg.strip("l=")
                if not l.isdigit():
                    print("argument: l, need to be a number")
                    return ["userInput"]
            if 'n=' in arg:
                n = arg.strip("n=")
                if not n.isdigit():
                    print("argument: n, need to be a number")
                    return ["userInput"]
            if arg == "r":
                r = True
    
        #create pw automatically
        new_pw = random_pw(l, n, r)
        
        save_account_to_db(user['name'], args[1], new_pw)
        return ["userInput"]

    #crate userdefined pw (not automatic)
    if user_defined:
        save_account_to_db(user['name'], args[1], args[2])
        return ["userInput"]

def show_pw(v, user):
    args = v
    res = []
    account = ""

    #check for correct syntax
    if not check_if_login(user):
        print("please login first")
        return ["userInput"]
    if len(args) <= 1:
        print("show needs at least a second argument")
        return ["userInput"]
    if args[1] != "name" and args[1] != "names":
        print("secont argument must be name or names")
        return ["userInput"]
    if args[1] == "name" and len(args) <= 2:
        print("third argument is needed")
        return ["userInput"]

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

        return ["userInput"]
    else:
        account = args[2]

        for t in res:
            if t[0] == account:
                print("account: ", t[0], "----> password: ", t[1])
                break
        
        return ["userInput"]

    print("no account: ", account, ", found")
    return ["userInput"]

def rm_account(v, user):
    if not check_if_login(user):
        print("login first")
        return ["userInput"]
    
    args = v
    username = ""
    account = ""
    success = False

    #check for correct syntax
    if len(args) <= 1:
        print("rm need an account which you want to remove")
        return ["userInput"]
    if len(args) > 2:
        print("you can only remove one account at a time")
        return ["userInput"]

    username = user['name']
    account = args[1]

    try:
        con = sqlite3.connect("../data/account.db")
        cur = con.cursor()

        res = cur.execute("DELETE FROM account WHERE name=? AND account=?", (username, account,))
        con.commit()
        success = True
    except Error as e:
        print("fail to remove account from db:", e)
        success = False
    finally:
        con.close()
    
    if success:
        print(account, ", was removed")
    else:
        print("something goes wrong :(")

    return ["userInput"]
        

# Main-Function
def main():
    q = False
    user = {'name': "", 'password': ""}
    v = ["userInput"]

    while not q:
        if v[0] == "userInput":
            v = userInput()
        elif v[0] == "h" or v[0] == "--help":
            v = showHelp()
            continue
        elif v[0] == "c":
            v = create_pw(v, user)
            continue
        elif v[0] == "show":
            v = show_pw(v, user)
        elif v[0] == "rm":
            v = rm_account(v, user)
        elif v[0] == "sign":
            v = sign()
        elif v[0] == "login":
            v = login(user)
            print(user)
        elif v[0] == "who":
            v = showCurrUser(user)
            continue
        elif v[0] == "q":
            q = True
        elif v[0] != "sign" and v[0] != "login":
            print("command: ", v, " not found")
            v = ["userInput"]

if __name__ == "__main__":
    main()
else:
    print("pwManager is the main program, don't use it as a module")



