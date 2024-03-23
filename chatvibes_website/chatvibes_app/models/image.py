from pathlib import Path

from django.db import models
from PIL import Image as PillowImage
from django.core.validators import MinValueValidator


from .word import Word
from .user import UserProfile
from .access_log import AccessLog
from ..storages import get_storage
from .legal import License, Copyright


class Image(AccessLog):
    image = models.ImageField(storage=get_storage)

    total_views = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    liked_by = models.ManyToManyField(UserProfile, blank=True, related_name="likes")
    bookmarked_by = models.ManyToManyField(UserProfile, blank=True, related_name="bookmarks")
    # todo add collections

    license = models.ForeignKey(License, default=None, blank=True, null=True, on_delete=models.RESTRICT)
    copyright = models.ForeignKey(Copyright, default=None, blank=True, null=True, on_delete=models.RESTRICT)

    nsfw = models.BooleanField(default=False)
    animated = models.BooleanField(default=False, editable=False)

    # TODO categories
    # subcategory = models.ForeignKey(Subcategory, on_delete=models.RESTRICT, related_name="emojis")
    tags = models.ManyToManyField(Word)

    def save(self, *args, **kwargs):
        self.animated = self.truly_animated
        super().save(args, kwargs)

    def __str__(self):
        return self.image.name

    @property
    def truly_animated(self) -> bool:
        return PillowImage.open(self.image.url).is_animated

    @property
    def total_likes(self) -> int:
        return self.liked_by.all().count()

    @property
    def bookmark_count(self) -> int:
        return self.bookmarked_by.all().count()

    @property
    def resolution(self) -> str:
        return f"{self.image.width}x{self.image.height}"

    @property
    def image_size(self) -> str:
        return f"{self.image.size}"

    @property
    def url(self) -> str:
        return self.image.url

    @property
    def extension(self) -> str:
        return Path(self.image.name).suffix[1:].lower()

    class Meta:
        ordering = ("date_create", )


class ImageCollection(AccessLog):
    images = models.ManyToManyField(Image, related_name="collections")
    is_private = models.BooleanField(
        default=False, help_text="Should it be visible on website or just for the user  that created it.")
