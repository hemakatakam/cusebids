from django.shortcuts import render
from .models import Item

# Create your views here.
def index(request):
    items = Item.objects.filter(active=True)
    return render(request, 'auction/index.html', {'items': items})

def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'auction/item_detail.html', {'item': item})