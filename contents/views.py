import os
import re
import mimetypes
import functools
import boto3
from wsgiref.util import FileWrapper
from io import BytesIO

from django.core.exceptions import FieldError
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views import View
from django.http.response import StreamingHttpResponse

from .models import Content, Detail
from wishlists.models import Wishlist
from my_settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET
from users.login_decorator import token_validation_decorator

class ContentView(View):
    @token_validation_decorator
    def get(self, request, content_id):
        try:
            content  = Content.objects.prefetch_related("genre", "details").get(id=content_id)
            wishlist = Wishlist.objects.filter(user = request.user, content = content, like=True).exists()
            result   = {
                "id"          : content.id,
                "name"        : content.name,
                "category"    : content.category,
                "description" : content.description,
                "nation"      : content.nation,
                "thumb_nail"  : content.thumb_nail,
                "wishlist"    : wishlist,
                "genre"       : [{"genre" : genre.name} for genre in content.genre.all()],
                "detail"      : [{
                    "detail_id"          : detail.id,
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

        except Content.DoesNotExist:
            return JsonResponse({"Result": "CONTENT_DOES_NOT_EXIST"}, status=404)

class MyS3Client:
    def __init__(self, s3_client, bucket):
        self.s3_client = s3_client
        self.bucket = bucket

    def get_video_file(self, video_path):
        return self.s3_client.get_object(Bucket = self.bucket, Key = video_path)

boto3_s3  = boto3.client("s3", region_name = 'ap-northeast-2', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
bucket    = BUCKET
s3_client = MyS3Client(boto3_s3, bucket)

class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=10240, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()

        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data

class ContentStreamingView(View):
    def get(self, request, detail_id):
        video_path = Detail.objects.get(id = detail_id).file
        video      = s3_client.get_video_file(video_path)
        size       = video.get("ContentLength")

        range_re   = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)

        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_match  = range_re.match(range_header)
        content_type, encoding = mimetypes.guess_type(video_path)
        content_type = content_type or 'application/octet-stream'

        if range_match:
            first_byte, last_byte = range_match.groups()

            first_byte = int(first_byte) if first_byte else 0
            last_byte = int(last_byte) if last_byte else size - 1

            if last_byte >= size:
                last_byte = size - 1

            length = last_byte - first_byte + 1
            result = StreamingHttpResponse(RangeFileWrapper(BytesIO(video["Body"].read()), offset=first_byte, length=length), status=206, content_type=content_type)
            result['Content-Length'] = str(length)
            result['Content-Range']  = 'bytes %s-%s/%s' % (first_byte, last_byte, size)

        else:
            result = StreamingHttpResponse(FileWrapper(BytesIO(video["Body"].read())), content_type=content_type)
            result['Content-Length'] = str(size)

        result['Accept-Ranges'] = 'bytes'
        result['X-Content-Type-Options'] = 'nosniff'
        
        return result
