from django.db import models
from core.models import TimeStampedModel

class Content(TimeStampedModel):
    name        = models.CharField(max_length=45)
    category    = models.CharField(max_length=45)
    description = models.CharField(max_length=400)
    nation      = models.CharField(max_length=45)
    thumb_nail  = models.URLField(max_length=300)
    genre       = models.ManyToManyField("Genre", related_name="contents", blank=True, through="ContentGenre")

    class Meta:
        db_table = "contents"

    def __str__(self):
        return self.name

class Detail(TimeStampedModel):
    episode      = models.CharField(max_length=45)
    description  = models.CharField(max_length=400)
    running_time = models.TimeField()
    thumb_nail   = models.URLField(max_length=300)
    file         = models.URLField(max_length=300)
    content      = models.ForeignKey("Content", on_delete=models.CASCADE, related_name="details")

    class Meta:
        db_table = "details"

    def __str__(self):
        return self.episode

class Genre(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "genres"

    def __str__(self):
        return self.name
class ContentGenre(models.Model):
    content = models.ForeignKey("Content", on_delete=models.CASCADE)
    genre   = models.ForeignKey("Genre", on_delete=models.CASCADE)

    class Meta:
        db_table = "content_genre_relations"