from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('myaccount/', views.myaccount, name = 'myaccount'),
    path('login/', auth_views.LoginView.as_view(template_name = 'userprofile/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('signup/', views.signup, name = 'signup'), 
    path('my_store/', views.my_store, name = 'my_store'),
    path('vendors/<int:pk>/', views.vendor_details, name = 'vendor_details'),
]