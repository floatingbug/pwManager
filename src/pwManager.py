#!/usr/bin/env python3.8

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

def createPassword(userInput, user):
    pw = ""

    if user['name'] == "":
        print("please login first")
        return "userInput"
    

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



