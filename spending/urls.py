from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('register_user/', views.register_user, name='register_user'),
    path('user_list/', login_required((views.UserListView), login_url='login_user'), name='user_list'),
    path('statistics/', login_required((views.StatisticsView), login_url='login_user'), name='statistics'),
    path('user_create/', login_required(views.UserCreateView.as_view(), login_url='login_user'), name='user_create'),
    path('user_update/<int:pk>', login_required(views.UserUpdateView.as_view(), login_url='login_user'), name='user_update'),
    path('user_delete/<int:pk>', login_required(views.UserDeleteView.as_view(), login_url='login_user'), name='user_delete'),
    path('delete_all_data/', login_required(views.delete_all_data, login_url='login_user'), name='delete_all_data'),
]
