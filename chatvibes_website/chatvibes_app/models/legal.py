from django.db import models

from .user import UserProfile
from .access_log import AccessLog


class License(AccessLog):
    abbreviation = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(unique=True, max_length=64)
    source_link = models.URLField(help_text="Optional link to license description.")

    def __str__(self):
        return self.abbreviation


class Copyright(AccessLog):
    # TODO either link or credit is required
    name = models.CharField(primary_key=True, max_length=32)
    link = models.URLField(help_text="Link to copyright source.")
    credits = models.TextField(max_length=512, default="", blank=True, help_text="Any additional credits.")

    def __str__(self):
        return self.name


class UserImageReport(AccessLog):
    reported_by = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL, related_name="reports")
    image = models.ForeignKey("Image", null=True, on_delete=models.SET_NULL, related_name="reports")
    reason = models.TextField(max_length=512, help_text="Reason for report.")
