from django import forms
from .models import Family

class FamilyGroupForm(forms.ModelForm):
    members = forms.CharField(widget=forms.Textarea, help_text="Enter usernames separated by commas")

    class Meta:
        model = Family
        fields = ['name', 'members']

class InviteMemberForm(forms.Form):
    usernames = forms.CharField(widget=forms.Textarea, help_text="Enter usernames separated by commas")