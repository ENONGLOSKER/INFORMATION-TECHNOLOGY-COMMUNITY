from django.shortcuts import render,redirect, get_object_or_404
from .models import Anggota,Sertifikat,Bidang,Pengurus,Program
from .forms import AnggotaForm,SertifikatForm,ProgramForm
from django.core.files.storage import default_storage
import os
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request,'home.html')
    
def index(request):
    bidangs = Bidang.objects.all()
    context = {
        'bidang': bidangs,
        }
    return render(request,'index.html',context)

# ANGGOTA
def anggota_create(request):
    if request.method == 'POST':
        form = AnggotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ITC_APP:anggota')
            # return redirect('anggota:anggota_detail', id=form.instance.id)
    else:
        form = AnggotaForm()

    return render(request, 'anggota_crate.html', {'form': form})

def anggota(request):
    data = Anggota.objects.all().order_by('-id')
    bidangs = Bidang.objects.all()

    context = {
        'datas':data,
        'bidang': bidangs,
    }
    return render(request,'anggota.html',context)

def anggota_detail(request,id):
    anggota = get_object_or_404(Anggota, id=id)

    context = {
        'anggota': anggota
    }
    return render(request,'anggota_detail.html',context)

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

def bidang_list(request):
    bidangs = Bidang.objects.all()
    context = {
        'bidang': bidangs,
        }
    return render(request, 'snippets/navbar.html',context )

def pengurus_list(request, id):
    bidangs = get_object_or_404(Bidang, id=id)
    pengurus = bidangs.bidang.all()
    return render(request, 'pengurus.html', {'bidangs': bidangs, 'pengurus': pengurus})


def program_add(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('program:program_list')
    else:
        form = ProgramForm()
    return render(request, 'program_create.html', {'form': form})

def program_add(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ITC_APP:program_list')  # Perbarui nama namespace
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