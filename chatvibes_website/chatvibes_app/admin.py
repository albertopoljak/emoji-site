from django.contrib import admin
from .models import image, legal, user, word


admin.site.register(image.Image)
admin.site.register(image.ImageCollection)

admin.site.register(legal.License)
admin.site.register(legal.Copyright)
admin.site.register(legal.UserImageReport)

admin.site.register(user.UserProfile)

admin.site.register(word.WordClassification)
admin.site.register(word.Word)


