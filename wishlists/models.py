from django.db import models
from core.models import TimeStampedModel

class Wishlist(TimeStampedModel):
    like        = models.BooleanField(default=True)
    user        = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="wishlists")
    content     = models.ForeignKey("contents.Content", on_delete=models.CASCADE, related_name="wishlists")

    class Meta:
        db_table = "wishlists"

    def __str__(self):
        return self.user + " like " + self.content