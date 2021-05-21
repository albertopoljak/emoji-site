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


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name="subcategories")
    name = models.CharField(
        primary_key=True,
        max_length=64,
        help_text="More specific, but still broad, version of category. Example anime show."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Subcategories"


class Emoji(models.Model):
    date_uploaded = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL, related_name="uploaded_emojis")

    favored_by = models.ManyToManyField(UserProfile, blank=True, related_name="favourites")
    bookmarked_by = models.ManyToManyField(UserProfile, blank=True, related_name="bookmarks")

    license = models.ForeignKey(EmojiLicense, on_delete=models.RESTRICT)
    source = models.URLField(default="", blank=True)
    credits = models.CharField(max_length=64, default="", blank=True)

    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name="emojis")
    sub_category = models.ForeignKey(Subcategory, on_delete=models.RESTRICT, related_name="emojis")

    downloads = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.image.name

    @property
    def animated(self) -> bool:
        return Image.open(self.image.url).is_animated

    @property
    def favorites_count(self) -> int:
        return self.favored_by.all().count()

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
