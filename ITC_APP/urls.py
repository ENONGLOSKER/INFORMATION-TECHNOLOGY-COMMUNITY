from django.urls import path
from .import views

app_name='ITC_APP'

urlpatterns = [
    path('',views.dashboard, name='dashboard'),
    path('anggota/',views.anggota, name='anggota'),
    path('anggota/create/',views.anggota_create, name='anggota_create'),
    path('anggota/detail/<int:id>',views.anggota_detail, name='anggota_detail'),
    path('anggota/delete/<int:id>',views.anggota_delete, name='anggota_delete'),
    path('anggota/update/<int:id>',views.anggota_update, name='anggota_update'),
    # sertifikat
    path('upload_sertifikat/', views.sertifikat_upload, name='upload_sertifikat'),
    path('lihat_sertifikat/', views.lihat_sertifikat, name='lihat_sertifikat'),
    # bidang
    path('bidang/', views.bidang_list, name='bidang'),
    path('bidang/setting/list/', views.bidang, name='bidang_list'),
    path('bidang/setting/update/<int:id>', views.bidang_update, name='bidang_update'),
    path('bidang/setting/delete/<int:id>', views.bidang_delete, name='bidang_delete'),
    path('bidang/setting/create/', views.bidang_create, name='bidang_create'),
    # pengurus
    path('pengurus/<int:id>', views.pengurus_list, name='pengurus'),
    path('pengurus/create/', views.pengurus_create, name='pengurus_create'),
    path('pengurus/update/<int:id>', views.pengurus_update, name='pengurus_update'),
    path('pengurus/delete/<int:id>', views.pengurus_delete, name='pengurus_delete'),
    # program
    path('add/', views.program_add, name='program_add'),
    path('list/', views.program_list, name='program_list'),
    path('events/', views.program_events, name='program_events'),
    path('calendar/', views.program_calendar, name='program_calendar'),

]
