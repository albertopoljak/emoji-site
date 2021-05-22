import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404

from .models import Emoji


EMOJI_PER_PAGE = 30


def index(request):
    all_emoji = Emoji.objects.all()[:EMOJI_PER_PAGE]
    context = {'all_emoji': all_emoji}
    return render(request, 'emoji_app/index.html', context)


def emoji_detail(request, emoji_id: int):
    emoji = get_object_or_404(Emoji, pk=emoji_id)
    context = {"emoji": emoji}
    return render(request, "emoji_app/detail.html", context)


@require_POST
def like(request, emoji_id: int):
    emoji = get_object_or_404(Emoji, pk=emoji_id)
    user = request.user

    if emoji.liked_by.filter(user=user).exists():
        emoji.liked_by.remove(user)
        message = "Successfully unliked."
    else:
        emoji.liked_by.add(user)
        message = "Successfully liked."

    context = {"likes_count": emoji.total_likes, "message": message}
    return HttpResponse(json.dumps(context), content_type="application/json")
