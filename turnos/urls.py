from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('canchas/', views.canchas, name='canchas'),
    path('agregar_cancha/', views.agregar_cancha, name='agregar_cancha'),
    path('detalle_cancha/<int:cancha_id>/', views.detalle_cancha, name='detalle_cancha'),
    path('reservar_turno/', views.reservar_turno, name='reservar_turno'),
    path('cancelar_turno/', views.cancelar_turno, name='cancelar_turno'),
    path('eliminar_cancha/<int:cancha_id>/', views.eliminar_cancha, name='eliminar_cancha'),
]