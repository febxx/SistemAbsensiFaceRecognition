from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from myapp.models import Karyawan, Presensi, Shift

import numpy as np
import os
# import requests
# from io import BytesIO
from PIL import Image
from math import *
# import efficientnet.tfkeras
# from tensorflow.keras.models import load_model
import face_recognition
import cv2
from datetime import date, datetime


def index(request):
    return render(request, 'index.html')

# =====================================================
#                       MODEL
# =====================================================

# parameters
# input_size = (150,150)
# channel = (3,)
# input_shape = input_size + channel
# labels = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

# def preprocess(img, input_size):
#     nimg = img.convert('RGB').resize(input_size, resample= 0)
#     img_arr = (np.array(nimg))/255
#     return img_arr

# def reshape(imgs_arr):
#     return np.stack(imgs_arr, axis=0)

# MODEL_PATH = './model/flowers/model.h5'
# model = load_model(MODEL_PATH, compile=False)


# =====================================================
#                       DASHBOARD
# =====================================================

@login_required
def dashboard(request):
    # l_media = os.listdir('./media/karyawan')
    # t_media = len(l_media)
    total = Karyawan.objects.all().count()
    print(total)
    context = {'total_karyawan': total}
    return render(request, 'dashboard.html', context)

def dataKaryawan(request):
    datas = Karyawan.objects.all()
    context = {'datas': datas}
    return render(request, 'karyawan.html', context)

def tambahData(request):
    if request.method == 'POST':

        # file = request.FILES['foto']
        # ext = file.name.split('.')[-1]
        # fs = FileSystemStorage()
        # filename = fs.save(file.name, file)
        # file_url = fs.url(filename)
        # print(filename)
        # print(ext)

        Karyawan(
            nip=request.POST['nip'],
            nama=request.POST['nama'],
            email=request.POST['email'],
            nohp=request.POST['nohp'],
            alamat=request.POST['alamat'],
            foto=request.FILES['foto'],
            jk=request.POST['jk'],
            jabatan=request.POST['jabatan']
        ).save()
        return redirect(tambahData)
    else:
        return render(request, 'tambahdata.html')

def hapusData(request, id):
    Karyawan.objects.get(id=id).delete()
    return redirect(dataKaryawan)

def dataAbsensi(request):
    return render(request, 'absensi.html')

def jamKerja(request):
    shifts = Shift.objects.all()
    print(shifts)
    if request.method == 'POST':
        print(request.POST)
        sh = Shift.objects.filter(id_shift=request.POST['id_shift'])
        if sh.exists():
            sh.update(
                awal_masuk = request.POST['awal_masuk'],
                masuk = request.POST['masuk'],
                akhir_masuk = request.POST['akhir_masuk'],
                awal_pulang = request.POST['awal_pulang'],
                pulang = request.POST['pulang'],
                akhir_pulang = request.POST['akhir_pulang']
            )
            # sh.save()
        else:
            Shift(
                id_shift = request.POST['id_shift'],
                awal_masuk = request.POST['awal_masuk'],
                masuk=request.POST['masuk'],
                akhir_masuk = request.POST['akhir_masuk'],
                awal_pulang = request.POST['awal_pulang'],
                pulang = request.POST['pulang'],
                akhir_pulang = request.POST['akhir_pulang']
            ).save()

    context = {'shifts': shifts}
    return render(request, 'jamkerja.html', context)

def hapusJamKerja(request, id):
    Shift.objects.get(id=id).delete()
    return redirect(jamKerja)

def scanViews(request):
    return render(request, 'captured.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user) 
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        
    return render(request, 'login.html')

def logoutView(request):
    logout(request)
    return redirect('index')


# =====================================================
#                     PREDICT IMAGE
# =====================================================

# def predictImage(request):
#     if request.method == 'POST':
#         print(request)
#         print(request.POST.dict())

#         fileObj = request.FILES['filePath']
#         fs = FileSystemStorage()
#         filePathName = fs.save(fileObj.name, fileObj)
#         filePathName = fs.url(filePathName)
#         testImage = '.'+filePathName

#         # predict
#         img = Image.open(testImage)
#         X = preprocess(img, input_size)
#         X = reshape([X])
#         y = model.predict(X)

#         predictedLabel = labels[np.argmax(y)]
#         predictedAcc = floor(np.max(y)*100)
#         print(predictedLabel)

#         context = {'filePathName':filePathName, 'predictedLabel':predictedLabel, 'acc':predictedAcc}
#         return render(request, 'captured.html', context)
#     else:
#         return redirect('/scan')


# =====================================================
#                     FACE RECOGNITION
# =====================================================

def openWebcam(request):
    video_capture = cv2.VideoCapture(0)

    karyawan = Karyawan.objects.all()
    names = []
    images = []
    files = []
    encodings = []

    for data in karyawan:
        names.append(data.nama)
        files.append('.'+data.foto.url)
        images.append(data.nama+'_image')
        encodings.append(data.nama+'_encoding')
    
    for i in range(0, len(files)):
        images[i] = face_recognition.load_image_file(files[i])
        encodings[i] = face_recognition.face_encodings(images[i])[0]

    known_face_encodings = encodings
    known_face_names = names
    counter = 0
    validate = ''
    today = date.today()
    while True:
        presensi = Presensi.objects.all()
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                print(name)

                if validate == '':
                    validate = name
                else:
                    if name == validate:
                        counter+=1
                    else:
                        validate = name
                        counter = 0

            # print(f'top: {top}, right: {right}, bottom: {bottom}, left: {left}')
            cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
            # cv2.rectangle(frame, (left, bottom-35), (right, bottom), (0,0,255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left - 50, top - 20), font, 1.0, (255, 255, 255), 1)

            data = Karyawan.objects.get(nama=name)
            now = datetime.now()
            # if now 
            shift = Shift.objects.get(id_shift=data.shift)
            if Presensi.objects.filter(nama=name, tanggal=today).exists():
                counter = 0
                cv2.putText(frame, 'Sudah Presensi', (left - 10, bottom + 40), font, 1.0, (255, 255, 255), 1)
            else:
                if counter >= 3:
                    data = Karyawan.objects.get(nama=name)
                    now = datetime.now().strftime('%H:%M:%S')
                    Presensi(
                        nip=data.nip,
                        nama=name,
                        tanggal=today,
                        check_in=now,
                        late_in=now,
                        check_out=now,
                        early_out=now,
                    ).save()
                    # cv2.putText(frame, 'Sudah Presensi', (left - 10, bottom + 40), font, 1.0, (255, 255, 255), 1)
                    # counter = 0
                
        cv2.imshow('Sistem Absensi', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return redirect(dashboard)