import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from agents.mixins import DirectorAndLoginRequiredMixin

from .forms import CategoryUpdateForm, LeadForm, MyUserCreationForm, PickAgentForm
from .models import Agent, Category, Lead


# Представление для Регистрации
class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = MyUserCreationForm

    def get_success_url(self):
        return reverse("login")


# Главная старница/Приветсвтенная страница
class RootPageView(generic.TemplateView):
    template_name = "root.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dash")
        return super().dispatch(request, *args, **kwargs)


# Страница с данными о лидах
class DashBoardView(DirectorAndLoginRequiredMixin, generic.TemplateView):
    template_name = "dash.html"

    def get_context_data(self, **kwargs):
        context = super(DashBoardView, self).get_context_data(**kwargs)

        user = self.request.user

        # Сколько всего лидов
        total_lead_count = Lead.objects.filter(company=user.userportfolio).count()

        # Сколько новых лидов за последние 30 дней
        thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)

        total_in_past30 = Lead.objects.filter(
            company=user.userportfolio, date_added__gte=thirty_days_ago
        ).count()

        # Сколько обращенных лидов за последние 30 дней
        converted_category = Category.objects.get(name="Обращенные")
        converted_in_past30 = Lead.objects.filter(
            company=user.userportfolio,
            category=converted_category,
            converted_date__gte=thirty_days_ago,
        ).count()

        context.update(
            {
                "total_lead_count": total_lead_count,
                "total_in_past30": total_in_past30,
                "converted_in_past30": converted_in_past30,
            }
        )
        return context


# Представление со списоком всех лидов. Надо улучшить frontend.
class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # первоначальный набор запросов лидов для всей компании
        if user.is_director:
            queryset = Lead.objects.filter(
                company=user.userportfolio, agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                company=user.agent.company, agent__isnull=False
            )
            # фильтрация для агента, который вошел в систему
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_director:
            queryset = Lead.objects.filter(
                company=user.userportfolio, agent__isnull=True
            )
            context.update(
                {
                    "unassigned_leads": queryset,
                }
            )
        return context


# Представление с подробностями каждого лида
class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        # первоначальный набор запросов лидов для всей компании
        if user.is_director:
            queryset = Lead.objects.filter(company=user.userportfolio)
        else:
            queryset = Lead.objects.filter(company=user.agent.company)
            # фильтрация для агента, который вошел в систему
            queryset = queryset.filter(agent__user=user)
        return queryset


# Представление для создание лидов.
class LeadCreateView(DirectorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.company = self.request.user.userportfolio
        lead.save()
        # Тут будет код для отправки электронной почты
        send_mail(
            subject="Только что был создан лид",
            message="Зайдите на сайт, чтобы посмотреть на нового лида",
            from_email="zhopa@mail.ru",
            recipient_list=["xuy@mail.ru"],
        )
        return super(LeadCreateView, self).form_valid(form)


# Представление для обновления(изменение данных и т.п.) лидов
class LeadUpdateView(DirectorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(company=user.userportfolio)

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "Вы успешно обновили этот лида")
        return super(LeadUpdateView, self).form_valid(form)


# Представление для удаленния лидов
class LeadDeleteView(DirectorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(company=user.userportfolio)

    def get_success_url(self):
        return reverse("leads:lead-list")


class PickAgentView(DirectorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/pick_agent.html"
    form_class = PickAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(PickAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update(
            {
                "request": self.request,
            }
        )
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(PickAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    # def get_context_data(self, **kwargs):
    #     user = self.request.user
    #     context = super(CategoryListView, self).get_context_data(**kwargs)

    #     if user.is_director:
    #         queryset = Lead.objects.filter(company=user.userportfolio)
    #     else:
    #         queryset = Lead.objects.filter(company=user.agent.company)

    #     context.update(
    #         {
    #             "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
    #         }
    #     )
    #     return context

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoryListView, self).get_context_data(**kwargs)
        cate_list = context["object_list"].values()
        list_of_categories = []

        if user.is_director:
            queryset = Lead.objects.filter(company=user.userportfolio)
        else:
            queryset = Lead.objects.filter(company=user.agent.company)
        for cate_number in cate_list:
            cate_number["number"] = queryset.filter(category=cate_number["id"]).count()
            x = {
                "id": cate_number["id"],
                "name": cate_number["name"],
                "number": cate_number["number"],
            }
            list_of_categories.append(x)

        context.update(
            {
                "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
                "reset": list_of_categories,
            }
        )
        return context

    def get_queryset(self):
        user = self.request.user
        # первоначальный набор запросов лидов для всей компании
        if user.is_director:
            queryset = Category.objects.filter(company=user.userportfolio)
        else:
            queryset = Category.objects.filter(company=user.agent.company)
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     leads = self.get_object().leads.all()
    #     context.update(
    #         {
    #             "leads": leads,
    #         }
    #     )
    #     return context

    def get_queryset(self):
        user = self.request.user
        # первоначальный набор запросов лидов для всей компании
        if user.is_director:
            queryset = Category.objects.filter(company=user.userportfolio)
        else:
            queryset = Category.objects.filter(company=user.agent.company)
        return queryset


class PickCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # первоначальный набор запросов лидов для всей компании
        if user.is_director:
            queryset = Lead.objects.filter(company=user.userportfolio)
        else:
            queryset = Lead.objects.filter(company=user.agent.company)
            # фильтрация для агента, который вошел в систему
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        lead_before_update = self.get_object()
        instance = form.save(commit=False)
        converted_category = Category.objects.get(name="Обращенные")
        if form.cleaned_data["category"] == converted_category:
            # обновить дату, когда этот лид был обращён.
            if lead_before_update.category != converted_category:
                # эта лид уже обращен
                instance.converted_date = datetime.datetime.now()
        instance.save()
        return super(PickCategoryUpdateView, self).form_valid(form)


# url names 3.05.49
# Class Based Views
