
from django.urls import path
from . import views
from allauth.account import views as allauth_views

urlpatterns = [
    path('', views.home, name='home'),
    path("admin-dashboard/children/", views.child_list, name="child_list"),
    path("admin-dashboard/staff/", views.staff_list, name="staff_list"),
     path("register-child/", views.register_child, name="register_child"),
    path("register-staff/", views.register_staff, name="register_staff"),

    path("admin-dashboard/children/<int:child_id>/delete/", views.delete_child, name="delete_child"),
    path("admin-dashboard/staff/<int:staff_id>/delete/", views.delete_staff, name="delete_staff"),


     path('donors/', views.donor_list, name='donor_list'),
    path('donors/add/', views.donor_add, name='donor_add'),
    path('donors/delete/<int:donor_id>/', views.donor_delete, name='donor_delete'),


    # Login and signup

    path('accounts/login/', allauth_views.LoginView.as_view(template_name='authentication/login.html'), name='account_login'),
    path('accounts/signup/', allauth_views.SignupView.as_view(template_name='authentication/signup.html'), name='account_signup'),
    path('accounts/logout/', allauth_views.LogoutView.as_view(), name='account_logout'),
    
]