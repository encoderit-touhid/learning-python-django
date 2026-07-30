from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("show-details/<slug:slug>/", views.show, name="show"),
    path("generate-slug/",views.generate_slug, name="generate-slug")   
    
]
