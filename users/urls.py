from django.urls import path

from users import views

urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('search', views.UserSearchView.as_view(), name='search'),
]