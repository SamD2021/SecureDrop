import userReg
import userLogin
import os


def main():
    main_loop()


def main_loop():
    while (True):
        command = input("secure_drop> ")
        if command == "help":
            help_command()
        else:
            print("Not a valid command, try one of the following: ")
            help_command()


def help_command():
    print('''    \"add\" -> Add a new contact
    \"list\" -> List all online contacts
    \"send\" -> Transfer file to contact
    \"exit\" -> Exit SecureDrop''')


if __name__ == '__main__':
    main()
