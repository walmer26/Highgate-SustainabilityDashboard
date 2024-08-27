from django.urls import path
from .views import profile_view, user_detail

app_name = 'users'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('detail/<str:username>/', user_detail, name='user_detail'),
]