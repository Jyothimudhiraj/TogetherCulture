from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("", views.home, name= "home"),
    path("AdminLogin/", views.AdminLogin, name="Admin"),
    path("AdminDashboard/", views.AdminDashboard, name="AdminDashboard"),
    path("UserRegistration/", views.UserRegistration, name="UserRegistration"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('allEvents/', views.EventsListing, name='EventsListing'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('update-membership/', views.update_membership, name='update_membership'),
    path('process/<str:email>/', views.process_membership, name='process_membership'),
    # path('AdminDashboard/', views.add_event, name='add_event'),
    path('api/add-event/', views.add_event_api, name='add_event_api'),
    path('search-members/', views.search_members, name='search_members'),
    path('profile/', views.profile, name='profile'),
    
    path('add-digital-content/', views.add_digital_content, name='add_digital_content'),
     path('digital-content/', views.view_digital_content, name='DigitalContent'),  # Keep this
    path('add-digital-content/', views.add_digital_content, name='add_digital_content'),
    path('register-digital-content/<int:content_id>/', views.register_digital_content, name='register_digital_content'),
    path('Benfits/', views.BenifitsandInterests, name='BenifitsAndInterests'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)