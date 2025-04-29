from home.views import index, people, PeopleAPI, PeopleViewSet, RegisterAPI, LoginAPI
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"people-viewset", PeopleViewSet, basename="people-viewset")
urlpatterns = [
    path("register/", RegisterAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("index/", index),
    path("person/", people),
    path("people-route/", PeopleAPI.as_view()),
    path("", include(router.urls))
]
