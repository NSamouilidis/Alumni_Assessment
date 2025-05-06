from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'alumni'

urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    # User profile
    path('profile/', views.profile, name='profile'),
    
    # Alumni directory
    path('directory/', views.AlumniListView.as_view(), name='alumni_list'),
    path('directory/<int:pk>/', views.AlumniDetailView.as_view(), name='alumni_detail'),
    
    # Schools
    path('schools/', views.SchoolListView.as_view(), name='school_list'),
    path('schools/<int:pk>/', views.SchoolDetailView.as_view(), name='school_detail'),
    
    # Events
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/register/', views.event_register, name='event_register'),
    
    # Admin area
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('alumni/<int:pk>/status/', views.AlumniStatusUpdateView.as_view(), name='alumni_status_update'),
    path('schools/create/', views.SchoolCreateView.as_view(), name='school_create'),
    path('schools/<int:pk>/update/', views.SchoolUpdateView.as_view(), name='school_update'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
]