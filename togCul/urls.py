from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("event-listing", views.event_listing, name="event-listing"),
    path("event-detail", views.event_detail, name="event-detail"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("approve-member/<int:member_id>/", views.approve_member, name="approve_member"),
    

    path("dashboard/notifications", views.page_notifications, name="page_notifications"),
    path("dashboard/tables", views.page_tables, name="page_tables"),
    path("dashboard/eventadd", views.add_event, name="eventadd"),
    path('dashboard/eventedit/<int:event_id>/', views.edit_event, name='eventedit'),
    path('dashboard/eventdelete/<int:event_id>/', views.delete_event, name='eventdelete'),


]
