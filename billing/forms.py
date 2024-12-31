from django import forms
from .models import CustomerModel


class CustomerCreationForm(forms.ModelForm):
    indexValue = forms.CharField()
    date = forms.DateField()
    igst = forms.IntegerField()
    
    class Meta:
        model = CustomerModel
        fields = ["igst","date","indexValue","username","email","address"]
        