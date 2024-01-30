from src.api.storage import BaseUserStorage


class UserService:
    def __init__(self, storage: BaseUserStorage):
        self.__storage = storage
