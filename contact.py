class Contact:
    def __init__(self, name="none", userid="none"):
        self.__container = {"UserID": userid, "Name": name}
        self.__online = False

    def get_name(self):
        return self.__container["Name"]

    def get_user_id(self):
        return self.__container["UserID"]

    def get_online_status(self) -> bool:
        return self.__online

    def set_name(self, name):
        self.__container["Name"] = name

    def set_user_id(self, user_id):
        self.__container["UserID"] = user_id

    def set_online_status(self, status: bool):
        self.__online = status
