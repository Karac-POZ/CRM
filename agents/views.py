import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from leads.models import Agent

from .forms import AgentForm
from .mixins import DirectorAndLoginRequiredMixin


class AgentListView(DirectorAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        company = self.request.user.userportfolio
        return Agent.objects.filter(company=company)


class AgentCreateView(DirectorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_director = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            company=self.request.user.userportfolio,
        )
        send_mail(
            subject="Приглашаем ВАС стать АГЕНТОМ!!!!!",
            message="ВЫ БЫЛИ ДОБАВЛЕНЫ КАК АГЕНТ В KaracCRM. ВОЙДИТЕ В СИСТЕМУ, ЧТОБЫ НАЧАТЬ РАБОТАТЬ",
            from_email="admin@mail.ru",
            recipient_list=[user.email],
        )
        # agent.company = self.request.user.userportfolio
        # agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(DirectorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        company = self.request.user.userportfolio
        return Agent.objects.filter(company=company)


class AgentUpdateView(DirectorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentForm

    def get_queryset(self):
        company = self.request.user.userportfolio
        return Agent.objects.filter(company=company)

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs["instance"] = kwargs["instance"].user
        return kwargs

    def get_success_url(self):
        return reverse("agents:agent-list")


class AgentDeleteView(DirectorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        company = self.request.user.userportfolio
        return Agent.objects.filter(company=company)
