from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # /accounts/signup/
    path('signup/', views.signup, name='signup'),
    # /accounts/signup/tourist/
    path('signup/tourist/', views.signup_tourist, name='signup_tourist'),
    # /accounts/signup/guide/
    path('signup/guide/', views.signup_guide, name='signup_guide'),
    
    # /accounts/login/
    path('login/', views.login, name='login'),
    # /accounts/logout/
    path('logout/', views.logout, name='logout'),
    
    # /accounts/harper/
    path('<str:username>/', views.profile, name='profile'),
    # /accounts/harper/wishlist/
    path('<str:username>/wishlist/', views.wishlist, name='wishlist'),
    # /accounts/harper/delete/
    path('<str:username>/delete/', views.delete, name='delete'),
]
