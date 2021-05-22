from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class UserProfile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class EmojiLicense(models.Model):
    name = models.CharField(unique=True, max_length=64)
    abbreviation = models.CharField(unique=True, max_length=16)
    source_link = models.URLField()

    def __str__(self):
        return self.abbreviation


class Category(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=32,
        help_text="Major category, for example Anime."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.SlugField(primary_key=True, max_length=16)
    category = models.ManyToManyField(Category, related_name="tags")

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(primary_key=True, max_length=32)
    link = models.URLField(help_text="Link to copyright source.")
    credits = models.TextField(max_length=512, default="", blank=True, help_text="Any additional credits.")

    def __str__(self):
        return self.name


class Emoji(models.Model):
    date_uploaded = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL, related_name="uploaded_emojis")

    liked_by = models.ManyToManyField(UserProfile, blank=True, related_name="likes")
    bookmarked_by = models.ManyToManyField(UserProfile, blank=True, related_name="bookmarks")

    license = models.ForeignKey(EmojiLicense, on_delete=models.RESTRICT)
    source = models.ForeignKey(Source, default=None, blank=True, null=True, on_delete=models.SET_NULL)

    tags = models.ManyToManyField(Tag, blank=True)

    downloads = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.image.name

    @property
    def animated(self) -> bool:
        return Image.open(self.image.url).is_animated

    @property
    def total_likes(self) -> int:
        return self.liked_by.all().count()

    @property
    def bookmark_count(self) -> int:
        return self.bookmarked_by.all().count()


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
        ordering = ('weight', )
        constraints = [
            models.UniqueConstraint(fields=['emoji', 'name'], name='unique emoji name')
        ]
