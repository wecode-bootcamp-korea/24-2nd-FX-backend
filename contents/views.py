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