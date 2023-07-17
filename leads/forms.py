from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import Agent, Lead

User = get_user_model()


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            "first_name",
            "last_name",
            "age",
            "agent",
            "review",
            "number",
            "email",
        )


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


class PickAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(company=request.user.userportfolio)
        super(PickAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ("category",)
