from pathlib import Path

from PIL import Image
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.deletion import SET_NULL, RESTRICT

from .users import UserProfile
from .legal import License, Source
from .sematics import Expression, Action
from emoji_site.emoji_app.storages import get_storage

# TODO add editable=False to fields (after debug phase)


class Category(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=32,
        help_text="Major category."
    )
    description = models.TextField(default="", blank=True, max_length=1024)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Subcategory(models.Model):
    """Subcategory can have multiple categories, for example
    Touhou can have both Anime and Game as a category"""
    name = models.SlugField(primary_key=True, max_length=64)
    categories = models.ManyToManyField(Category, related_name="subcategories")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Subcategories"


class EmojiClassification(models.Model):
    name = models.SlugField(primary_key=True, max_length=64)
    subcategory = models.ForeignKey(Subcategory, on_delete=RESTRICT)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Character(EmojiClassification):
    pass


class Object(EmojiClassification):
    pass


class Emoji(models.Model):
    date_uploaded = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(UserProfile, null=True, on_delete=SET_NULL, related_name="uploaded_emojis")

    image = models.ImageField(storage=get_storage)
    views = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    downloads = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    liked_by = models.ManyToManyField(UserProfile, blank=True, related_name="likes")
    bookmarked_by = models.ManyToManyField(UserProfile, blank=True, related_name="bookmarks")

    license = models.ForeignKey(License, on_delete=models.RESTRICT)
    source = models.ForeignKey(Source, default=None, blank=True, null=True, on_delete=models.RESTRICT)

    animated = models.BooleanField(default=False, editable=False)
    nsfw = models.BooleanField(default=False)

    subcategory = models.ForeignKey(Subcategory, on_delete=models.RESTRICT, related_name="emojis")
    characters = models.ManyToManyField(Character, related_name="emojis", help_text=(
        "Usually 1 for characters but emoji can have multiple (rem&ram).",
        "Includes characters (Koishi, golem, vampire, Michael Jordan) and animals."
    ))
    objects = models.ManyToManyField(
        Character, related_name="emojis",
        help_text="If character has any object (like knife), or if this is an object itself"
    )
    expressions = models.ManyToManyField(Expression, help_text="Like smile, sad etc")
    actions = models.ManyToManyField(Action, help_text="Like explode, stab, dance etc")

    def save(self, *args, **kwargs):
        self.animated = self.truly_animated
        super().save(args, kwargs)

    def __str__(self):
        return self.image.name

    @property
    def truly_animated(self) -> bool:
        return Image.open(self.image.url).is_animated

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
    def size(self) -> str:
        return f"{self.image.size}"

    @property
    def url(self) -> str:
        return self.image.url

    @property
    def extension(self) -> str:
        return Path(self.image.name).suffix[1:].lower()

    class Meta:
        ordering = ("date_uploaded", )


class RecommendedName(models.Model):
    emoji = models.ForeignKey(Emoji, related_name="names", on_delete=models.CASCADE)
    weight = models.SmallIntegerField(validators=[MinValueValidator(0)])
    name = models.SlugField(
        max_length=32,
        help_text="Recommend name for this emoji."
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("weight", )
        constraints = [
            models.UniqueConstraint(fields=["emoji", "name"], name="unique emoji name"),
            models.UniqueConstraint(fields=["emoji", "weight", "name"], name="unique emoji weight")
        ]
