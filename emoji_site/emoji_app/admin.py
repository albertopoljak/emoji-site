from django.contrib import admin
from .models import UserProfile, EmojiLicense, Category, Tag, Source, Emoji, RecommendedName


class RecommendedNamesInline(admin.TabularInline):
    model = RecommendedName


class EmojiAdmin(admin.ModelAdmin):
    exclude = ("favored_by", "bookmarked_by",)
    readonly_fields = ("date_uploaded", "downloads",)
    inlines = [RecommendedNamesInline]


admin.site.register(Emoji, EmojiAdmin)

admin.site.register(UserProfile)
admin.site.register(EmojiLicense)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Source)
admin.site.register(RecommendedName)
