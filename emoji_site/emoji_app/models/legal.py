from django.db import models
from django.db.models.deletion import SET_NULL

from .users import UserProfile
from .emoji import Emoji


class License(models.Model):
    name = models.CharField(unique=True, max_length=64)
    abbreviation = models.CharField(unique=True, max_length=16)
    source_link = models.URLField()

    def __str__(self):
        return self.abbreviation


class Source(models.Model):
    name = models.CharField(primary_key=True, max_length=32)
    link = models.URLField(help_text="Link to copyright source.")
    credits = models.TextField(max_length=512, default="", blank=True, help_text="Any additional credits.")

    def __str__(self):
        return self.name


class EmojiReports(models.Model):
    reported_by = models.ForeignKey(UserProfile, null=True, on_delete=SET_NULL, related_name="reports")
    emoji = models.ForeignKey(Emoji, null=True, on_delete=SET_NULL, related_name="reports")
    reason = models.TextField(max_length=512, help_text="Reason for report.")
