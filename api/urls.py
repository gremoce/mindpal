from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("pomodoro/", views.pomodoro, name="pomodoro"),
    path("chat/", views.chat, name="chat"),
    path('resources/', views.resources_page, name='resources'),

]
