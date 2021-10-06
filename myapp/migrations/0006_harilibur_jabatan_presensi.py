# Generated by Django 3.2.5 on 2021-09-22 11:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_karyawan_foto'),
    ]

    operations = [
        migrations.CreateModel(
            name='HariLibur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hari', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Jabatan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_jabatan', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Presensi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nip', models.CharField(max_length=18)),
                ('nama', models.CharField(max_length=255)),
                ('tanggal', models.DateField(default=datetime.date.today)),
                ('check_in', models.TimeField()),
                ('late_in', models.TimeField()),
                ('check_out', models.TimeField()),
                ('early_out', models.TimeField()),
                ('ket', models.CharField(max_length=100)),
                ('suhu', models.CharField(max_length=5)),
            ],
        ),
    ]