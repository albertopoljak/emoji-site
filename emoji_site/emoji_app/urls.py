from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:emoji_id>/', views.emoji_detail, name='detail'),
    path('like/<int:emoji_id>/', views.emoji_detail, name='like')
]
