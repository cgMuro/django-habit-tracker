from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login_request'),
    path('logout/', views.logout_request, name='logout_request'),
    path('add-habit/', views.add_habit, name='add_habit'),
    path('update-habit/<int:habit_id>', views.update_habit, name='update_habit'),
    path('delete-habit/<int:habit_id>', views.delete_habit, name='delete_habit')
]