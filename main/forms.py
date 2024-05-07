from .models import Record
from django import forms

class RecordUpdateForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = "set_date", "unset_date", "description"
        localized_fields = ('set_date', 'unset_date')

class CustomerRecordNewForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = "product", "set_date", "description"
        localized_fields = ('set_date', )
        widgets = {
            "set_date": forms.DateInput(attrs={'type': 'date'}),
            # "unset_date": forms.DateInput(attrs={'type': 'date'}),
        }

class ProductRecordNewForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = "customer", "set_date", "description"
        localized_fields = ('set_date', )
        widgets = {
            "set_date": forms.DateInput(attrs={'type': 'date'}),
        }
