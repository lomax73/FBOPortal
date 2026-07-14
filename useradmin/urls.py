from django.urls import path

from . import views

urlpatterns = [
    path('utenti/', views.user_list, name='user-list'),
    path('utenti/nuovo/', views.user_create, name='user-create'),
    path('utenti/<int:app_pk>/<int:user_id>/modifica/', views.user_update, name='user-update'),
    path('utenti/<int:app_pk>/<int:user_id>/elimina/', views.user_delete, name='user-delete'),
]
