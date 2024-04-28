from django.forms import ModelForm
from .models import Listing
from django.core.exceptions import ValidationError

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'initial', 'image', 'category']
        
    def clean(self):
        super().clean()  
        if self.cleaned_data.get('initial') <= 0:
            raise ValidationError({'initial': 'The initial price must be greater than zero.'})
        return self.cleaned_data
 