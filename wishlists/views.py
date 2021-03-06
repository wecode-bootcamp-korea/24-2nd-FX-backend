import json

from django.http import JsonResponse
from django.views import View
from django.db import transaction

from wishlists.models import Wishlist
from contents.models import Content
from users.models import User
from users.login_decorator import token_validation_decorator

class WishListView(View):
    @token_validation_decorator
    def patch(self, request):
        try:
            data       = json.loads(request.body)
            content_id = data.get("content_id")
            user       = request.user
            content    = Content.objects.get(id = content_id)

            with transaction.atomic():
                wish, created = Wishlist.objects.get_or_create(user = user, content = content)

                if not created:
                    wish.like = not wish.like
                    wish.save()

                result = {
                    "user_id"    : user.id,
                    "content_id" : content_id,
                    "like"       : wish.like,
                }

                return JsonResponse({"Result": result}, status=206)

        except Content.DoesNotExist:
            return JsonResponse({"Result": "CONTENT_DOES_NOT_EXIST"}, status=404)

    @token_validation_decorator
    def get(self, request):
        wishlists =  Wishlist.objects.filter(user=request.user, like = True).select_related('content').prefetch_related('content__genre')

        result  = [{
            "content_id"  : wishlist.content.id,
            "name"        : wishlist.content.name,
            "category"    : wishlist.content.category,
            "description" : wishlist.content.description,
            "nation"      : wishlist.content.nation,
            "thumb_nail"  : wishlist.content.thumb_nail,
            "genre"       : [{"genre" : genre.name} for genre in wishlist.content.genre.all()],
        } for wishlist in wishlists]

        return JsonResponse({"Result": result}, status=200)
