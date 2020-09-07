from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('delete/<int:pk>', views.delete_user, name='delete_user'),
]



