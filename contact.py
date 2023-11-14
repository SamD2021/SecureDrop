class Contact:
    def __init__(self, name='none', userid='none'):
        self.__container = {'UserID': userid, 'Name': name}

    def get_name(self):
        return self.__container['Name']

    def get_user_id(self):
        return self.__container['UserID']

    def set_name(self, name):
        self.__container['Name'] = name

    def set_user_id(self, user_id):
        self.__container['UserID'] = user_id
