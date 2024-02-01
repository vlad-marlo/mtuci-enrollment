from src.api.storage import BaseStorage


class NotesService:
    def __init__(self, storage: BaseStorage):
        self.__storage = storage
