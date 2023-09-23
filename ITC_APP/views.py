from django.shortcuts import render,redirect, get_object_or_404
from .models import Anggota,Sertifikat,Bidang,Pengurus,Program
from .forms import AnggotaForm,SertifikatForm,ProgramForm,PengurusForm,BidangForm
from django.core.files.storage import default_storage
import os
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse


# Create your views here.

@csrf_exempt
def dashboard(request):
    bidangs = Bidang.objects.all()
    context = {
        'bidang': bidangs,
        }
    return render(request,'dashboard.html',context)

# ANGGOTA

@csrf_exempt
def anggota_create(request):
    bidang = Bidang.objects.all()
    if request.method == 'POST':
        form = AnggotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Data Berhasil di Tambahkan!")
            return redirect('dashboard:anggota')
            # return redirect('anggota:anggota_detail', id=form.instance.id)
    else:
        form = AnggotaForm()

    context = {
        'form': form,
        'bidang': bidang,
    }
    return render(request, 'anggota_crate.html',context)
@csrf_exempt
def anggota(request):
    data = Anggota.objects.all().order_by('-id')
    bidangs = Bidang.objects.all()

    context = {
        'datas':data,
        'bidang': bidangs,
    }

    if request.method == 'POST':
        anggota_id = request.POST.get('anggota_id')  # Pastikan tombol verifikasi memiliki name="anggota_id"
        anggota = Anggota.objects.get(id=anggota_id)
        anggota.diverifikasi = not anggota.diverifikasi  # Toggle status diverifikasi
        anggota.save()
        
    return render(request,'anggota.html',context)
@csrf_exempt
def anggota_update(request,id):
    bidang = Bidang.objects.all()
    anggota = get_object_or_404(Anggota, id=id)
    if request.method == 'POST':
        form = AnggotaForm(request.POST, instance=anggota)

        if form.is_valid():
            form.save()
            messages.success(request, " Data Berhasil di Update!")
            return redirect('dashboard:anggota')
    else:
        form = AnggotaForm(instance=anggota)
    
    context ={
        'form': form,
        'bidang': bidang,
    }

    return render(request, 'anggota_crate.html',context )
@csrf_exempt
def anggota_detail(request,id):
    bidang = Bidang.objects.all()
    anggota = get_object_or_404(Anggota, id=id)

    context = {
        'anggota': anggota,
        'bidang': bidang,
    }
    return render(request,'anggota_detail.html',context)
@csrf_exempt
def anggota_delete(request,id):
    anggota = get_object_or_404(Anggota, id=id)
    anggota.delete()
    return redirect('dashboard:anggota')

#bidang
def bidang_list(request):
    bidangs = Bidang.objects.all()
    context = {
        'bidang': bidangs,
        }
    return render(request, 'snippets/navbar.html',context )

def bidang(request):
    bidangs = Bidang.objects.all()
    context = {
        'bidang': bidangs,
        }
    return render(request, 'bidang.html',context )

def bidang_create(request):
    bidang = Bidang.objects.all()
    if request.method == 'POST':
        form = BidangForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Data Berhasil di Tambah!")
            return redirect('dashboard:bidang_list')
    else:
        form = BidangForm()

    context = {
        'form': form,
        'bidang': bidang,
    }
    return render(request, 'bidang_create.html',context)

def bidang_update(request,id):
    bidang = Bidang.objects.all()
    bidangs = get_object_or_404(Bidang, id=id)
    if request.method == 'POST':
        form = BidangForm(request.POST, instance=bidangs)

        if form.is_valid():
            form.save()
            messages.success(request, " Data Berhasil di Update!")
            return redirect('dashboard:bidang_list')
    else:
        form = BidangForm(instance=bidangs)
    
    context ={
        'form': form,
        'bidang': bidang,
    }

    return render(request, 'bidang_create.html',context )

def bidang_delete(request,id):
    bidang = get_object_or_404(Bidang, id=id)
    bidang.delete()
    return redirect('dashboard:bidang_list')

# pengurus
def pengurus_list(request, id):
    bidang = Bidang.objects.all()
    bidangs = get_object_or_404(Bidang, id=id)
    pengurus = bidangs.bidang.all()
    context={
        'bidangs': bidangs, 
        'bidang': bidang, 
        'pengurus': pengurus,
    }

    return render(request, 'pengurus.html',context )

def pengurus_create(request):
    bidang = Bidang.objects.all()
    if request.method == 'POST':
        form = PengurusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Data Berhasil di Tambah!")
            return redirect('dashboard:bidang')
    else:
        form = PengurusForm()

    context = {
        'form': form,
        'bidang': bidang,
    }
    return render(request, 'pengurus_crate.html',context)

def pengurus_update(request,id):
    bidang = Bidang.objects.all()
    pengurus = get_object_or_404(Pengurus, id=id)
    if request.method == 'POST':
        form = PengurusForm(request.POST, instance=pengurus)

        if form.is_valid():
            form.save()
            messages.success(request, " Data Berhasil di Update!")
            return redirect('dashboard:anggota')
    else:
        form = PengurusForm(instance=pengurus)
    
    context ={
        'form': form,
        'bidang': bidang,
    }

    return render(request, 'pengurus_crate.html',context )

def pengurus_delete(request,id):
    pengurus = get_object_or_404(Pengurus, id=id)
    pengurus.delete()
    return redirect('dashboard:anggota')

# sertifikat
def sertifikat_upload(request):
    if request.method == 'POST':
        form = SertifikatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect ke halaman sertifikat setelah berhasil menyimpan
            return redirect('lihat_sertifikat')
    else:
        form = SertifikatForm()
    
    return render(request, 'sertifikat_upload.html', {'form': form})

def lihat_sertifikat(request):
    sertifikat_list = Sertifikat.objects.all()
    return render(request, 'sertifikat.html', {'data': sertifikat_list})

# program
def program_add(request):
    bidangs = Bidang.objects.all()
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Data Berhasil di Tambah!")
            return redirect('program:program_list')
    else:
        form = ProgramForm()
    return render(request, 'program_create.html', {'form': form})

def program_add(request):
    bidangs = Bidang.objects.all()
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:program_list')  # Perbarui nama namespace
    else:
        form = ProgramForm()
    return render(request, 'program_add.html', {'form': form})

def program_list(request):
    programs = Program.objects.all()
    return render(request, 'program_list.html', {'programs': programs})

def program_events(request):
    programs = Program.objects.all()
    events = []

    for program in programs:
        events.append({
            'title': program.nama_program,
            'start': program.start_date.strftime('%Y-%m-%d'),
            'end': program.end_date.strftime('%Y-%m-%d'),
            'location': program.lokasi_program,
            'description': program.keterangan
        })

    return JsonResponse(events, safe=False)

def program_calendar(request):
    return render(request, 'program_calendar.html')