from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('response/', views.chat_response, name='chat_response'),
]