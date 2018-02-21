from django import forms

from experimenter.experiments.models import Experiment


class ExperimentForm(forms.ModelForm):
    name = forms.CharField(help_text=Experiment.NAME_HELP_TEXT, widget=forms.TextInput(attrs={'class': 'form-control'}))
    short_description = forms.CharField(help_text=Experiment.SHORT_DESCRIPTION_HELP_TEXT, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    population_percent = forms.DecimalField(help_text=Experiment.POPULATION_PERCENT_HELP_TEXT, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    firefox_version = forms.ChoiceField(choices=Experiment.VERSION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    firefox_channel = forms.ChoiceField(choices=Experiment.CHANNEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    client_matching = forms.CharField(help_text=Experiment.CLIENT_MATCHING_HELP_TEXT, initial=Experiment.CLIENT_MATCHING_DEFAULT, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Experiment
        exclude = []
