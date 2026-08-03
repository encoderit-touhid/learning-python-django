from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("show-details/<slug:slug>/", views.show, name="show"),
    path("generate-slug/",views.generate_slug, name="generate-slug"),   
    path("test/",views.test, name="test"),   
    path("test-many-to-many/",views.many_to_many, name="test-many-to-many"),   
    path("n-plus-one/", views.n_plus_one_demo, name="n-plus-one"),
    path("field-selection/", views.field_selection_demo, name="field-selection")
]
