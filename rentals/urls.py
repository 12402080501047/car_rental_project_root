from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cars/', views.car_list_view, name='car_list'),
    path('confirm-booking/<int:car_id>/', views.confirm_booking_view, name='confirm_booking'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
    path('my-cancel-booking/<int:booking_id>/', views.my_cancel_booking_view, name='my_cancel_booking'),
]
