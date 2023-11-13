class Contact:
    def __init__(self, full_name='none', email_address='none'):
        self.__full_name = full_name
        self.__email_address = email_address

    def get_full_name(self):
        return self.__full_name

    def get_email_address(self):
        return self.__email_address

    def set_full_name(self, full_name):
        self.__full_name = full_name

    def set_email_address(self, email_address):
        self.__email_address = email_address
