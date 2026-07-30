from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="challenges-index"),
    # path("template/", views.template_rendering),
    path("<int:month>/", views.dynamic_month_by_index),
    path("<str:month>/", views.dynamic_month_by_name, name="monthly-challenges"),
]

