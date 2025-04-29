from home.views import index, people, login, PeopleAPI, PeopleViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"people-viewset", PeopleViewSet, basename="people-viewset")
urlpatterns = [
    path("index/", index),
    path("person/", people),
    path("login/", login),
    path("people-route/", PeopleAPI.as_view()),
    path("", include(router.urls))
]
