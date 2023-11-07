import userReg
import userLogin
import os
import json
import fc
from contact import Contact


class SecureDrop:
    def __init__(self):
        self.__contacts = {}
        self.__contact_info = "contacts.json"

    def add_command(self):
        # Inside your method
        full_name = input("Enter Full Name: ")
        email_address = input("Enter Email Address: ")

        new_contact = Contact(full_name, email_address)

        # Store Contact instance in the dictionary using the email address as key
        self.__contacts[email_address] = new_contact

        # Write the dictionary of contacts to a file in JSON format
        with open(self.__contact_info, 'w') as file:
            contacts_data = {email: contact.get_full_name() for email, contact in self.__contacts.items()}
            json.dump(contacts_data, file)

def main():
    my_secure_drop = SecureDrop()
    main_loop(my_secure_drop)


def help_command():
    print('''    \"add\" -> Add a new contact
    \"list\" -> List all online contacts
    \"send\" -> Transfer file to contact
    \"exit\" -> Exit SecureDrop''')


def main_loop(user_secure_drop):
    while True:
        command = input("secure_drop> ")
        if command.lower() == "help":
            help_command()
        elif command.lower() == "add":
            user_secure_drop.add_command()
        elif command.lower() == "exit":
            break
        else:
            print("Not a valid command, try one of the following: ")
            help_command()


if __name__ == '__main__':
    main()
