from django.db import models
from django.db.models.deletion import RESTRICT


class Word(models.Model):
    noun = models.CharField()
    adjective = models.CharField()
    base_synonym = models.ForeignKey("Word", on_delete=RESTRICT)

    @property
    def is_noun(self) -> bool:
        # name HAS to be a noun, use API to find out, if it isn't block saving
        return False

    @property
    def adjective_from_api(self) -> str:
        # adjective, if not set, should be auto fetched from API
        return ""

    @property
    def is_base_synonym(self) -> bool:
        return self.base_synonym is None

    class Meta:
        abstract = True


class Expression(Word):
    pass


class Action(Word):
    pass
