from django.urls import path

from . import views

urlpatterns = [
    path('rack-report/', views.ProgettoListView.as_view(), name='progetto-list'),
    path('rack-report/nuovo/', views.ProgettoCreateView.as_view(), name='progetto-create'),
    path('rack-report/<int:pk>/', views.ProgettoDetailView.as_view(), name='progetto-detail'),
    path('rack-report/<int:pk>/modifica/', views.ProgettoUpdateView.as_view(), name='progetto-update'),
    path('rack-report/<int:pk>/elimina/', views.ProgettoDeleteView.as_view(), name='progetto-delete'),
    path('rack-report/<int:pk>/report.pdf', views.progetto_report_pdf, name='progetto-report-pdf'),

    path('rack-report/<int:progetto_pk>/rack/nuovo/', views.RackCreateView.as_view(), name='rack-create'),
    path('rack/<int:pk>/modifica/', views.RackUpdateView.as_view(), name='rack-update'),
    path('rack/<int:pk>/elimina/', views.RackDeleteView.as_view(), name='rack-delete'),
    path('rack/<int:pk>/allegati/carica/', views.rack_allegato_upload, name='rack-allegato-upload'),
    path('rack-allegato/<int:pk>/elimina/', views.RackAllegatoDeleteView.as_view(), name='rack-allegato-delete'),

    path('rack/<int:rack_pk>/elemento/nuovo/', views.ElementoRackCreateView.as_view(), name='elemento-create'),
    path('elemento/<int:pk>/modifica/', views.ElementoRackUpdateView.as_view(), name='elemento-update'),
    path('elemento/<int:pk>/elimina/', views.ElementoRackDeleteView.as_view(), name='elemento-delete'),
    path('elemento/<int:pk>/posizioni/', views.elemento_posizioni, name='elemento-posizioni'),
]
