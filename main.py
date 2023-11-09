import userReg
import userLogin
import os
import json
from contact import Contact


class SecureDrop:
    def __init__(self, user_id="Guest"):
        self.__user_id = user_id
        self.__contacts = {}
        self.__contact_info = "contacts.json"

    def main_loop(self):
        while True:
            command = input("secure_drop> ")
            if command.lower() == "help":
                self.help_command()
            elif command.lower() == "add":
                self.add_command()
            elif command.lower() == "exit":
                break
            else:
                print("Not a valid command, try one of the following: ")
                self.help_command()

    @staticmethod
    def help_command():
        print('''    \"add\" -> Add a new contact
        \"list\" -> List all online contacts
        \"send\" -> Transfer file to contact
        \"exit\" -> Exit SecureDrop''')

    def add_command(self):
        # Inside your method
        full_name = input("Enter Full Name: ").title()
        email_address = input("Enter Email Address: ").lower()

        new_contact = Contact(full_name, email_address)

        # Store Contact instance in the dictionary using the email address as key
        self.__contacts[email_address] = new_contact

        # Write the dictionary of contacts to a file in JSON format
        with open(self.__contact_info, 'w') as file:
            contacts_data = {email: contact.get_full_name() for email, contact in self.__contacts.items()}
            json.dump(contacts_data, file)


def main():
    # Check if needs to register or login
    my_secure_drop = SecureDrop()
    my_secure_drop.main_loop()


if __name__ == '__main__':
    main()
