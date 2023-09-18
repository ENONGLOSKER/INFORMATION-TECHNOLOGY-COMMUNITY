from django.contrib import admin
from .models import Anggota,Sertifikat, Bidang, Pengurus,Program

# # Register your models here.
admin.site.register(Anggota)
admin.site.register(Sertifikat)
admin.site.register(Bidang)
admin.site.register(Pengurus)
admin.site.register(Program)