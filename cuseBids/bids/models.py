from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2)
    current_bid = models.DecimalField(max_digits=9, decimal_places=2)
    image_url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items_owned')
    active = models.BooleanField(default=True)

class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids_made')
    bid_amount = models.DecimalField(max_digits=9, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
