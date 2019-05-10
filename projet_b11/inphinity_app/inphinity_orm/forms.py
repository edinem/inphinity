from django import forms
from .models import *


class FamilyForm(forms.ModelForm):

    class Meta:
        model = Family
        fields = ('designation', )


class ScoreCalculationForm(forms.ModelForm):

    class scoreCalcForm(forms.ModelForm):
        taxonomie = forms.ModelMultipleChoiceField(queryset=LevelInteraction.objects.all())


