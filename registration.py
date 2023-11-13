# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from getpass import getpass


def getInfo():
    fullName: str = input("Enter Full Name: ").lower().capitalize().capitalize()
    email = input("Enter Email Address: ").lower()
    password = getpass("Enter Password: ")
    matchPassword = getpass("Re-enter Password: ")
    while password != matchPassword:
        print("Mismatched Passwords, Try again!")
        password = getpass("Enter Password: ")
        matchPassword = getpass("Re-enter Password: ")
    print("Passwords Match.")
    return fullName, email, password

# Press the green button in the gutter to run the script.
