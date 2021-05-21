from django.contrib import admin
from .models import UserProfile, EmojiLicense, Category, Subcategory, Emoji, RecommendedName

admin.site.register(UserProfile)
admin.site.register(EmojiLicense)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(RecommendedName)


@admin.register(Emoji)
class EmojiAdmin(admin.ModelAdmin):
    exclude = ("favored_by", "bookmarked_by",)
    readonly_fields = ("date_uploaded", "downloads",)
