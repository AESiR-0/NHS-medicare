from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Agency URLs
    path('nurses/', views.nurse_list, name='nurse_list'),
    path('nurses/create/', views.nurse_create, name='nurse_create'),
    path('nurses/<int:nurse_id>/documents/', views.nurse_document_upload, name='nurse_document_upload'),
    
    # Hospital URLs
    path('shifts/create/', views.shift_create, name='shift_create'),
    path('shifts/', views.shift_list, name='shift_list'),
    
    # Agency Shift URLs
    path('available-shifts/', views.available_shifts, name='available_shifts'),
    path('shifts/<int:shift_id>/book/', views.book_shift, name='book_shift'),
    
    # Admin URLs
    path('admin/nurses/<int:nurse_id>/approve/', views.approve_nurse, name='approve_nurse'),
    path('admin/agency-trust/<int:access_id>/approve/', views.approve_agency_trust, name='approve_agency_trust'),
] 