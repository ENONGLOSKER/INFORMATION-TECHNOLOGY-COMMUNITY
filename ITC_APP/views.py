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
    jlh_anggota = Anggota.objects.all().count()
    bid_nav = Bidang.objects.all()

    data_pengurus_per_bidang = []
    bidangs = Bidang.objects.all()

    for bidang in bidangs:
        jumlah_pengurus = Pengurus.objects.filter(bidang=bidang).count()
        data_pengurus_per_bidang.append({
            'nama_bidang': bidang.nama_bidang,
            'jumlah_pengurus': jumlah_pengurus,
        })

    context = {
        'bid_nav': bid_nav,
        'jlh_anggota': jlh_anggota,
        'data_pengurus_per_bidang': data_pengurus_per_bidang,
    }

    return render(request, 'dashboard.html', context)



# ANGGOTA

@csrf_exempt
def anggota_create(request):
    bid_nav = Bidang.objects.all()
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
        'bid_nav': bid_nav,
    }
    return render(request, 'anggota_crate.html',context)
@csrf_exempt
def anggota(request):
    data = Anggota.objects.all().order_by('-id')
    bid_nav = Bidang.objects.all()

    context = {
        'datas':data,
        'bid_nav': bid_nav,
    }

    if request.method == 'POST':
        anggota_id = request.POST.get('anggota_id')  # Pastikan tombol verifikasi memiliki name="anggota_id"
        anggota = Anggota.objects.get(id=anggota_id)
        anggota.diverifikasi = not anggota.diverifikasi  # Toggle status diverifikasi
        anggota.save()
        
    return render(request,'anggota.html',context)
@csrf_exempt
def anggota_update(request,id):
    bid_nav = Bidang.objects.all()
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
        'bid_nav': bid_navbid_nav,
    }

    return render(request, 'anggota_crate.html',context )
@csrf_exempt
def anggota_detail(request,id):
    bid_nav = Bidang.objects.all()
    anggota = get_object_or_404(Anggota, id=id)

    context = {
        'anggota': anggota,
        'bid_nav': bid_nav,
    }
    return render(request,'anggota_detail.html',context)
@csrf_exempt
def anggota_delete(request,id):
    anggota = get_object_or_404(Anggota, id=id)
    anggota.delete()
    return redirect('dashboard:anggota')

#bidang
def bidang_list(request):
    bid_nav = Bidang.objects.all()
    context = {
        'bidang': bid_nav,
        }
    return render(request, 'snippets/navbar.html',context )

def bidang(request):
    bid_nav = Bidang.objects.all()
    context = {
        'bidang': bid_nav,
        }
    return render(request, 'bidang.html',context )

def bidang_create(request):
    bid_nav = Bidang.objects.all()
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
        'bid_nav': bid_nav,
    }
    return render(request, 'bidang_create.html',context)

def bidang_update(request,id):
    bid_nav = Bidang.objects.all()
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
        'bid_nav': bid_nav,
    }

    return render(request, 'bidang_create.html',context )

def bidang_delete(request,id):
    bidang = get_object_or_404(Bidang, id=id)
    bidang.delete()
    return redirect('dashboard:bidang_list')

# pengurus
def pengurus_list(request, id):
    bid_nav = Bidang.objects.all()
    bidangs = get_object_or_404(Bidang, id=id)
    pengurus = bidangs.bidang.all()
    context={
        'bidangs': bidangs, 
        'bid_nav': bid_nav, 
        'pengurus': pengurus,
    }

    return render(request, 'pengurus.html',context )

def pengurus_create(request):
    bid_nav = Bidang.objects.all()
    if request.method == 'POST':
        form = PengurusForm(request.POST)
        if form.is_valid():
            pengurus = form.save()  # Simpan objek pengurus ke dalam variabel
            messages.success(request, "Data Berhasil di Tambah!")
            return redirect('dashboard:pengurus', id=pengurus.bidang.id)  # Redirect ke pengurus bidang yang sesuai
    else:
        form = PengurusForm()

    context = {
        'form': form,
        'bid_nav': bid_nav,
    }
    return render(request, 'pengurus_crate.html',context)


def pengurus_update(request,id):
    bid_nav = Bidang.objects.all()
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
        'bid_nav': bid_nav,
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