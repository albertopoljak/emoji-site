from django.db import models
from crum import get_current_user
from django.utils import timezone
from django.contrib.auth.models import User


class AccessLog(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    date_write = models.DateTimeField(auto_now_add=True)

    create_user = models.ForeignKey(
        User, editable=False, blank=True, null=True, on_delete=models.SET_NULL, related_name="+")
    write_user = models.ForeignKey(
        User, editable=False, blank=True, null=True, on_delete=models.SET_NULL, related_name="+")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None

        if self._state.adding:
            self.create_user = user

        self.date_write = timezone.now()
        self.write_user = user
        super().save(*args, **kwargs)
