from django.urls import path

from .views import (
    CategoryDetailView,
    CategoryListView,
    LeadCreateView,
    LeadDeleteView,
    LeadDetailView,
    LeadListView,
    LeadUpdateView,
    PickAgentView,
    PickCategoryUpdateView,
)

app_name = "leads"

urlpatterns = [
    path("", LeadListView.as_view(), name="lead-list"),
    path("<int:pk>/", LeadDetailView.as_view(), name="lead-detail"),
    path("<int:pk>/update/", LeadUpdateView.as_view(), name="lead-update"),
    path("<int:pk>/delete/", LeadDeleteView.as_view(), name="lead-delete"),
    path("<int:pk>/pick-agent/", PickAgentView.as_view(), name="pick-agent"),
    path(
        "<int:pk>/category/", PickCategoryUpdateView.as_view(), name="category-update"
    ),
    path("create/", LeadCreateView.as_view(), name="lead-create"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
]
