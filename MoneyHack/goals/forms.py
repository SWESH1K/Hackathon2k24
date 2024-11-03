from django import forms
from .models import Goal
from django.db import models

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'target_amount', 'weightage', 'due_date', 'icon']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(GoalForm, self).__init__(*args, **kwargs)

    def clean_weightage(self):
        weightage = self.cleaned_data.get('weightage')
        if self.user:
            total_weightage = Goal.objects.filter(user=self.user).aggregate(total=models.Sum('weightage'))['total'] or 0
            if self.instance.pk:
                # If editing an existing goal, subtract its current weightage from the total
                total_weightage -= self.instance.weightage
            if total_weightage + weightage > 100:
                raise forms.ValidationError('The total weightage of all goals cannot exceed 100%.')
        return weightage