from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta: # Setting up the Meta Data
        model = Room
        fields = '__all__' # Specifying to have ALL fields