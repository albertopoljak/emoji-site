from django.conf import settings
from django.core.files.storage import Storage, FileSystemStorage


class LocalEmojiStorage(FileSystemStorage):
    def __init__(self):
        super().__init__(location="./media/emoji")


def get_storage() -> Storage:
    if not settings.DEBUG:
        raise NotImplementedError("Emoji storage not yet implemented for production use.")

    return LocalEmojiStorage()
