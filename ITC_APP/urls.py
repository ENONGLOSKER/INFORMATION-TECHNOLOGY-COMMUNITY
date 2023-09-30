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
    path('print_preview/', views.print_preview, name='print_preview'),
    path('update_cetak_status/', views.update_cetak_status, name='update_cetak_status'),

   
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

    path('calendar/list', views.calendar, name='calendar'), 
    path('all_events/', views.all_events, name='all_events'), 
    path('calendar/', views.calendar_view, name='program_calendar'),
    path('add_event/', views.add_event, name='add_event'),
    path('remove_event/<int:event_id>/', views.remove_event, name='remove_event'),
    path('update_program/', views.update_program, name='update_program'),
    # path('remove/', views.remove, name='remove'),
    # path('edit_event/<int:id>/', views.edit_event, name='edit_event'),
    # path('get_event_details/', views.get_event_details, name='get_event_details'),
    # path('edit_or_delete_event/<int:event_id>/', views.edit_or_delete_event, name='edit_or_delete_event'),


]
