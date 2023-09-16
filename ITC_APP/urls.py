from django.urls import path
from .import views

app_name='ITC_APP'

urlpatterns = [
    path('',views.index, name='index'),
    path('home/',views.home, name='home'),
    path('anggota/',views.anggota, name='anggota'),
    path('anggota/create/',views.anggota_create, name='anggota_create'),
    path('anggota/<int:id>',views.anggota_detail, name='anggota_detail'),
]
