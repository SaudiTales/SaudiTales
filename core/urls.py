from django.urls import path, include
from . import views
from django.conf import settings
from django.http import HttpResponseForbidden

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('exploreResult/', views.exploreResult, name='exploreResult'),
    # path('infoPlace/', views.infoPlace, name='infoPlace'),
    path('profile/', views.profile, name='profile'),

    #registeration:
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path("logout/", views.logout_view, name="logout"),

    #admin dashboard:
    path('dashboard/', views.dashboard, name='dashboard'),
    path('landmarks/', views.landmarks, name='landmarks'),
    path('accountMang/', views.accountMange, name='AccountManagement'),

    # for AI Landmark Recognition Model
    path('predict/', views.predict_landmark, name='predict_landmark'),

    path('infoPlace/<int:landmark_id>/', views.infoPlace, name='infoPlace'),
    path('toggle_favorite/<int:landmark_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('delete_landmark/<int:landmark_id>/', views.delete_landmark, name='delete_landmark'),
    path('add_landmark/', views.add_landmark, name='add_landmark'),
    path('update_landmark/<int:landmark_id>/', views.update_landmark, name='update_landmark'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('disable_user/<int:id>/', views.disable_user, name='disable_user'),
    path('enable_user/<int:id>/', views.enable_user, name='enable_user'),
    path('accounts/', include('django.contrib.auth.urls')),
]