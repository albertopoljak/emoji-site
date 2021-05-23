from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "emoji_app"
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:emoji_id>/', views.emoji_detail, name='detail')
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
