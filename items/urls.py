from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('lost/', views.lost_items_view, name='lost_items'),
    path('lost/new/', views.create_lost_view, name='create_lost'),
    path('lost/<int:pk>/', views.lost_detail_view, name='lost_detail'),
    path('lost/<int:pk>/edit/', views.edit_lost_view, name='edit_lost'),
    path('lost/<int:pk>/delete/', views.delete_lost_view, name='delete_lost'),
    path('lost/<int:pk>/mark-found/', views.mark_lost_found_view, name='mark_lost_found'),

    path('found/', views.found_items_view, name='found_items'),
    path('found/new/', views.create_found_view, name='create_found'),
    path('found/<int:pk>/', views.found_detail_view, name='found_detail'),
    path('found/<int:pk>/edit/', views.edit_found_view, name='edit_found'),
    path('found/<int:pk>/delete/', views.delete_found_view, name='delete_found'),
    path('found/<int:pk>/mark-returned/', views.mark_found_returned_view, name='mark_found_returned'),

    path('match/<str:kind>/<int:pk>/', views.report_match_view, name='report_match'),

    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read_view, name='mark_notification_read'),

    path('api/search/', views.search_api_view, name='search_api'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
]
