from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('new/', views.create_entry, name='create_entry'),
    path('<int:pk>/', views.entry_detail, name='entry_detail'),
    path('edit/<int:pk>/', views.edit_entry, name='edit_entry'),
    path('delete/<int:pk>/', views.delete_entry, name='delete_entry'),
    path('search/', views.search_entries, name='search_entries'),
]
