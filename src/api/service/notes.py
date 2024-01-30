from src.api.storage import BaseNotesStorage


class NotesService:
    def __init__(self, storage: BaseNotesStorage):
        self.__storage = storage
