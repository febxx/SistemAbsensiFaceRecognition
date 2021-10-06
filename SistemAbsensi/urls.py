from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('karyawan', views.dataKaryawan, name='karyawan'),
    path('tambahdata', views.tambahData, name='tambahdata'),
    path('hapusdata/<int:id>', views.hapusData, name='hapusdata'),
    path('absensi', views.dataAbsensi, name='absensi'),
    path('jamkerja', views.jamKerja, name='jamkerja'),
    path('hapusshift/<int:id>', views.hapusJamKerja, name='hapusshift'),
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('scan', views.scanViews, name='scan'),
    # path('predictImage', views.predictImage, name='predictImage'),
    path('openwebcam', views.openWebcam, name='openWebcam'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)