from src.api.storage import BaseStorage


class RevisionService:
    def __init__(self, storage: BaseStorage):
        self.__storage = storage
