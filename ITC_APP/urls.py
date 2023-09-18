from django.urls import path
from .import views

app_name='ITC_APP'

urlpatterns = [
    path('',views.index, name='index'),
    path('home/',views.home, name='home'),
    path('anggota/',views.anggota, name='anggota'),
    path('anggota/create/',views.anggota_create, name='anggota_create'),
    path('anggota/<int:id>',views.anggota_detail, name='anggota_detail'),
    path('upload_sertifikat/', views.sertifikat_upload, name='upload_sertifikat'),
    path('lihat_sertifikat/', views.lihat_sertifikat, name='lihat_sertifikat'),
    # bidang
    path('bidang/', views.bidang_list, name='bidang'),
    path('pengurus/<int:id>', views.pengurus_list, name='pengurus'),
    # program
    path('add/', views.program_add, name='program_add'),
    path('list/', views.program_list, name='program_list'),
    path('events/', views.program_events, name='program_events'),
    path('calendar/', views.program_calendar, name='program_calendar'),

]
