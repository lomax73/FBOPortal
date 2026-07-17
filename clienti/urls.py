from django.urls import path

from . import views

urlpatterns = [
    path('clienti/', views.ClienteListView.as_view(), name='cliente-list'),
    path('clienti/nuovo/', views.ClienteCreateView.as_view(), name='cliente-create'),
    path('clienti/<uuid:pk>/modifica/', views.ClienteUpdateView.as_view(), name='cliente-update'),
    path('clienti/<uuid:pk>/elimina/', views.ClienteDeleteView.as_view(), name='cliente-delete'),

    path('api/internal/clienti/', views.InternalClienteListView.as_view(), name='internal-cliente-list'),
    path('api/internal/clienti/<uuid:pk>/', views.InternalClienteDetailView.as_view(), name='internal-cliente-detail'),
]
