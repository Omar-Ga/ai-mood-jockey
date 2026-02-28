from django.urls import path
from . import views

app_name = 'playlist_generator'

urlpatterns = [
    path('generate/', views.generate_playlist, name='generate_playlist'),
    path('api/status/', views.api_status, name='api_status'),
    path('api/public/generate/', views.public_generate_playlist, name='public_generate_playlist'),
    path('api/query/<int:query_id>/', views.get_query, name='get_query'),
    path('api/query/<int:query_id>/delete/', views.delete_query, name='delete_query'),
]
