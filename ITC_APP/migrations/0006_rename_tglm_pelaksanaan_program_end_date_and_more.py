# Generated by Django 4.1.5 on 2023-09-17 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ITC_APP', '0005_program'),
    ]

    operations = [
        migrations.RenameField(
            model_name='program',
            old_name='tglM_pelaksanaan',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='program',
            old_name='tglS_pelaksanaan',
            new_name='start_date',
        ),
    ]
