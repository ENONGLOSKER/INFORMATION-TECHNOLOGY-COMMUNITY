# Generated by Django 4.1.5 on 2023-10-05 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ITC_APP', '0015_alter_anggota_nomor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anggota',
            name='cetak',
        ),
        migrations.AddField(
            model_name='anggota',
            name='tanggal_diverifikasi',
            field=models.DateField(blank=True, null=True),
        ),
    ]
