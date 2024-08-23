from django.urls import path
from . import views

urlpatterns = [
path('',views.index,name="login"),
path('signup/',views.signup,name="signup"),
path("gpt/",views.GPT,name='gpt'),
path('logout/',views.logout,name='logout'),
path('chat/', views.chat_view, name='chat_view'),
]