import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Emoji


EMOJI_PER_PAGE = 30


def index(request):
    all_emoji = Emoji.objects.all()[:EMOJI_PER_PAGE]
    context = {'all_emoji': all_emoji}
    return render(request, 'emoji_app/index.html', context)


@require_http_methods(["GET", "POST"])
def emoji_detail(request, emoji_id: int):
    if request.method == 'GET':
        emoji = get_object_or_404(Emoji, pk=emoji_id)
        context = {"emoji": emoji}
        return render(request, "emoji_app/detail.html", context)
    elif request.method == 'POST':
        return _like_emoji(request, emoji_id)


def _like_emoji(request, emoji_id: int):
    emoji = get_object_or_404(Emoji, pk=emoji_id)
    user_profile = request.user.profile

    if emoji.liked_by.filter(id=user_profile.id).exists():
        emoji.liked_by.remove(user_profile)
        message = "Removed like"
    else:
        emoji.liked_by.add(user_profile)
        message = "Added like."

    context = {"likes_count": emoji.total_likes, "message": message}
    return HttpResponse(json.dumps(context), content_type="application/json")
