from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'tag', 'way_of_payment', 'transaction_type']

class UploadFileForm(forms.Form):
    file = forms.FileField()