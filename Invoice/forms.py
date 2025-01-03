from django import forms
from .models import letter_information,list_of_items

class Letter_info_form(forms.ModelForm):
    class Meta:
        model=letter_information
        fields=['address','returnable','source','destination','name']

class Add_items_form(forms.ModelForm):
    class Meta:
        model=list_of_items
        fields=['description','quantity']



        