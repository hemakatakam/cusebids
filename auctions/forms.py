from django.forms import ModelForm
from .models import Listing
from django.core.exceptions import ValidationError

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'initial', 'image', 'category']
        
    def clean(self):
        super().clean()  # Don't forget to clean the form first
        if not self.cleaned_data.get('initial') <= 0:
            raise ValidationError('Listing details are not valid, ensure the name is not empty and the price is greater than zero.')
        return self.cleaned_data
