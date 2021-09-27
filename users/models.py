from django.db import models
from core.models import TimeStampedModel


class User(TimeStampedModel):
    class SignupType(models.IntegerChoices):
        FLIX   = 1
        KAKAO  = 2
        GOOGLE = 3

    name        = models.CharField(max_length=45)
    email       = models.EmailField(max_length=100, null=True ,blank=True)
    password    = models.CharField(max_length=500)
    signup_type = models.CharField(max_length=10, choices=SignupType.choices, default=SignupType.FLIX)
    kakao_id    = models.CharField(max_length=100, blank=True, null=True, unique=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name

class UserDetail(models.Model):
    user          = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_details")
    detail        = models.ForeignKey("contents.Detail", on_delete=models.CASCADE, related_name="user_details")
    watching_time = models.TimeField(null=True)

    class Meta:
        db_table = "user_detail_relations"