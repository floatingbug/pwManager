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

    try:
        con = sqlite3.connect("../data/shadow.db")
        cur = con.cursor()

        res = cur.execute("SELECT * FROM users WHERE name='?'", (name))
    
        print(res.fetchone())
        return sign
    except Error as e:
        print("fail: ", e)
    finally:
        con.close()


def main():
    q = False
    user = {}
    v = userInput()
    
    while not q:
        if v == "h" or v == "--help":
            showHelp()
            v = userInput()
        elif v == "sign":
            sign()
        elif v == "q":
            q = True
        else:
            print("command: ", v, " not found")
            v = userInput()

if __name__ == "__main__":
    main()
else:
    print("pwManager is the main program, don't use it as a module")



