from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name="index"),
    path("blogs/",views.blog_grid, name="blog-grid"),
    path("blogs/<slug:slug>/",views.blog_single, name="single-details")
]
