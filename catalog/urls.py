from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('stato-app/', views.app_status_list, name='app-status-list'),
    path('stati/', views.status_config_list, name='status-config-list'),
    path('stati/nuovo/', views.status_config_create, name='status-config-create'),
    path('stati/<int:pk>/modifica/', views.status_config_update, name='status-config-update'),
    path('stati/<int:pk>/elimina/', views.status_config_delete, name='status-config-delete'),
]
