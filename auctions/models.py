from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    CATEGORIES = [
        ('Accessories', 'Accessories'),
        ('Antiques', 'Antiques'),
        ('Clothes', 'Clothes'),
        ('Decoration', 'Decoration'),
        ('Electronics', 'Electronics'),
        ('Valuables', 'Valueables'),
        ('Other', 'Other'),
    ]
    STATUS = [
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
    ]
    DEFAULT_USER = 1
    name = models.CharField(max_length = 100, blank = False)
    initial = models.DecimalField(max_digits = 10, decimal_places = 2)
    user = models.ForeignKey(User, blank = False, on_delete = models.CASCADE, default = DEFAULT_USER)
    image = models.ImageField(default = 'None/NIA.png')
    category = models.CharField(max_length = 11, choices = CATEGORIES, default = 'Other')
    status = models.CharField(max_length = 7, choices = STATUS, default = 'Pending')
    created = models.DateField(auto_now_add = True)

    def __str__(self):
        return f"{self.name} - starts at ${self.initial}"

    
    def is_valid_listing(self):
        return self._check_name() and self._check_initial_price()

    def _check_name(self):
        return len(self.name) > 0

    def _check_initial_price(self):
        return self.initial > 0
    
    def display_status(self):
        if self.status == 'Pending':
            return "This listing is still open."
        elif self.status == 'Closed':
            return "This listing has been closed."


class Bid(models.Model):
    user = models.ForeignKey(User, blank = False, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, blank = False, on_delete = models.CASCADE)
    highest_bid = models.DecimalField(max_digits = 10, decimal_places = 2)
    added = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"${self.highest_bid} - {self.user} on {self.listing.name}"



class Comment(models.Model):
    user = models.ForeignKey(User, blank = False, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, blank = False, on_delete = models.CASCADE)
    comment = models.CharField(max_length = 400, blank = False)
    added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.comment} - by {self.user}"
