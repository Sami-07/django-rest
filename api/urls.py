from home.views import index, people, login, PeopleAPI
from django.urls import path

urlpatterns = [
    path("index/", index),
    path("person/", people),
    path("login/", login),
    path("people-route/", PeopleAPI.as_view())
]
