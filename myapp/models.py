from django.db import models
import os
from datetime import date, datetime

# Create your models here.

def rename(instance, filename):
    directory = 'karyawan'
    ext = filename.split('.')[-1]
    filename = f'{instance.nama}.{ext}'
    return os.path.join(directory, filename)

class Karyawan(models.Model):
    nip = models.CharField(max_length=18)
    nama = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    nohp = models.CharField(max_length=12)
    alamat = models.TextField(blank=True)
    foto = models.ImageField(upload_to=rename)
    jk = models.CharField(max_length=1)
    jabatan = models.CharField(max_length=200)
    shift = models.CharField(max_length=2, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.nama}'

class Presensi(models.Model):
    nip = models.CharField(max_length=18)
    nama = models.CharField(max_length=255)
    tanggal = models.DateField()
    check_in = models.TimeField()
    late_in = models.CharField(max_length=3)
    check_out = models.TimeField()
    early_out = models.CharField(max_length=3)
    ket = models.CharField(max_length=100)
    suhu = models.CharField(max_length=5) 

class Jabatan(models.Model):
    nama_jabatan = models.CharField(max_length=100)

class HariLibur(models.Model):
    hari = models.CharField(max_length=10)

class Shift(models.Model):
    id_shift = models.CharField(max_length=2)
    awal_masuk = models.TimeField()
    masuk = models.TimeField()
    akhir_masuk = models.TimeField()
    awal_pulang = models.TimeField()
    pulang = models.TimeField()
    akhir_pulang = models.TimeField()

