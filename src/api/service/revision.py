from src.api.storage import BaseRevisionsStorage


class RevisionService:
    def __init__(self, storage: BaseRevisionsStorage):
        self.__storage = storage
