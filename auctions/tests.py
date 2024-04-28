from django.test import Client, TestCase

from .models import Listing, Bid, User

class ListingTestCase(TestCase):

    def setUp(self):

        user = User.objects.create(username="foo", password="baz", email="foo@baz.com")

        l1 = Listing.objects.create(name="dummy1", initial=100, category="Other")
        l2 = Listing.objects.create(name="dummy2", initial=200, category="Accessories")

        Bid.objects.create(user=user, listing=l1, highest_bid=110)
        Bid.objects.create(user=user, listing=l2, highest_bid=210)
        Bid.objects.create(user=user, listing=l1, highest_bid=130)

    def test_bid_count(self):
        l = Listing.objects.get(initial=100)
        bids = Bid.objects.filter(listing=l).count()
        self.assertEqual(bids, 2)

    def test_valid_listing(self):
        l = Listing.objects.get(name="dummy1")
        self.assertTrue(l.is_valid_listing())

    def test_invalid_listing(self):
        l = Listing.objects.create(name="", initial=0)
        self.assertFalse(l.is_valid_listing())

    def test_index_page(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
