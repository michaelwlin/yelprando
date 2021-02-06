from django.urls import path
from . import views

urlpatterns = [
    path ('', views.searchpage),
    path ('createuser',views.createuser),
    path ('search',views.searchpage),
    path ('search_randomize',views.search_randomize),
    path ('result',views.result),
    path ('noresult',views.noresult),
    path ('randomize_again',views.randomize_again),
    path ('clear',views.clear),
]