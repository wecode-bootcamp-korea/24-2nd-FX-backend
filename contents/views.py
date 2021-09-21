import functools

from django.core.exceptions import FieldError
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views import View

from .models import Content

class ContentView(View):
    def get(self, request, content_id):
        try:
            content = Content.objects.prefetch_related("genre", "details").get(id=content_id)
            result  = {
                "id"          : content.id,
                "name"        : content.name,
                "category"    : content.category,
                "description" : content.description,
                "nation"      : content.nation,
                "thumb_nail"  : content.thumb_nail,
                "genre"       : [{"genre" : genre.name} for genre in content.genre.all()],
                "detail"      : [{
                    "episode"            : detail.episode,
                    "detail_description" : detail.description,
                    "running_time"       : detail.running_time,
                    "detail_thumb_nail"  : detail.thumb_nail,
                    } for detail in content.details.all()]
            }

            return JsonResponse({"Result": result}, status=200)

        except Content.DoesNotExist:
            return JsonResponse({"Result": "CONTENT_DOES_NOT_EXIST"}, status=404)

class ContentListView(View):
    def get(self, request):
        try:
            ORDER_BY   = request.GET.get("order-by", "?")
            LIMIT      = int(request.GET.get("limit", 10))
            CATEGORIES = request.GET.getlist("category")
            NATION     = request.GET.getlist("nation")
            GENRE      = request.GET.getlist("genre")

            FILTERS = {
            "category"   : Q(category__in =CATEGORIES),
            "nation"     : Q(nation__in=NATION),
            "genre"      : Q(genre__name__in=GENRE),
            }

            query    = functools.reduce(lambda q1, q2: q1.add(q2, Q.AND), [FILTERS.get(key, Q()) for key in request.GET.keys()], Q())
            contents = Content.objects.filter(query).annotate(hot = Count('wishlists')).order_by(ORDER_BY).prefetch_related("genre")[:LIMIT]

            result   = [{
                "id"          : content.id,
                "name"        : content.name,
                "category"    : content.category,
                "description" : content.description,
                "nation"      : content.nation,
                "thumb_nail"  : content.thumb_nail,
                "genre"       : [{"genre" : genre.name} for genre in content.genre.all()],
                } for content in contents]

            return JsonResponse({"Result": result}, status=200)

        except FieldError:
            return JsonResponse({"Result": "FIELD_ERROR"}, status=404)