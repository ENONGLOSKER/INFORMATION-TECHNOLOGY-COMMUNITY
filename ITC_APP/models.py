# models.py
import qrcode
from django.db import models
from django.urls import reverse
import os
from django.conf import settings


class Anggota(models.Model):
    nama     = models.CharField(max_length=255)
    jk       = models.CharField(max_length=255)
    alamat   = models.TextField()
    nim      = models.IntegerField()
    prodi    = models.CharField(max_length=255)
    semester = models.CharField(max_length=255)
    nomor    = models.IntegerField()
    email    = models.CharField(max_length=255)
    qr       = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        qr_data = f'Nama: {self.nama}\nJK: {self.jk}\nAlamat: {self.alamat}\nNIM: {self.nim}\nProdi: {self.prodi}\nSemester: {self.semester}\nNomor: {self.nomor}\nEmail: {self.email}'

        qr = qrcode.QRCode(
            version=1, 
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        img_path = os.path.join('qrcodes', f'{self.id}.png')
        img.save(os.path.join(settings.MEDIA_ROOT, img_path))

        self.qr = img_path
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('anggota_detail', args=[str(self.id)])

class Sertifikat(models.Model):
    e_sertifikat = models.FileField(upload_to='sertifikat/')

    def __str__(self):
        return self.e_sertifikat.name

class Bidang(models.Model):
    nama_bidang = models.CharField(max_length=255)
    deskripsi = models.TextField()

    def __str__(self):
        return self.nama_bidang

class Pengurus(models.Model):
    status = models.CharField(max_length=255)
    nama_pengurus = models.ForeignKey(Anggota, on_delete=models.CASCADE, related_name='anggota')
    bidang  = models.ForeignKey(Bidang, on_delete=models.CASCADE, related_name='bidang')

    def __str__(self):
        return self.status

class Program(models.Model):
    nama_program = models.CharField(max_length=255)
    jenis_program = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    lokasi_program = models.CharField(max_length=255)
    waktu = models.CharField(max_length=255)
    keterangan = models.TextField()