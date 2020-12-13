from django.urls import path
from . import views

urlpatterns = [
    path('callback', views.callback),
    path('test',views.send_message_test)
]