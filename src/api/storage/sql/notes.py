from src.api.storage.abs import BaseNotesStorage
from src.core.models import Note


class NotesStorage(BaseNotesStorage):
    def __init__(self):
        pass

    async def create(self, note: Note) -> Note:
        """create stores note to system"""
        pass

    async def update(self, note: Note) -> Note:
        """update updates note and returns changed Note to user"""
        pass

    async def delete(self, note: Note) -> None:
        """deletes note"""
        pass

    async def get_all_by_user_id_with_status(
            self,
            user_id: int,
            status: int,
    ) -> list[Note]:
        """
        return all notes, related to user with status.

        Statuses:
        -1 Not
        """
        pass

    async def get_all_by_user_id(self, user_id: int) -> list[Note]:
        """return all notes, related to user with provided id"""
        pass

