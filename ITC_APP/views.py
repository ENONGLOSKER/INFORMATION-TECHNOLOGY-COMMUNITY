from django.shortcuts import render,redirect, get_object_or_404
from .models import Anggota,Sertifikat,Bidang,Pengurus,Program,Event
from .forms import AnggotaForm,SertifikatForm,ProgramForm,PengurusForm,BidangForm
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone

import json

from django.http import JsonResponse

def update_cetak_status(request):
    if request.method == 'POST':
        anggota_id = request.POST.get('anggota_id')
        is_checked = request.POST.get('isChecked')

        anggota = Anggota.objects.get(id=anggota_id)
        anggota.cetak = is_checked
        anggota.save()

        return JsonResponse({'message': 'Status cetak diperbarui'}, status=200)
    else:
        return JsonResponse({'message': 'Metode permintaan tidak valid'}, status=400)


def print_preview(request):
    if request.method == 'POST':
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        Anggota.objects.filter(id__in=selected_ids).update(cetak=True)

        return HttpResponse(status=200)

    return HttpResponseBadRequest('Invalid request method')

@login_required()
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
@login_required()
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
@login_required()
@csrf_exempt
def anggota(request):
    data = Anggota.objects.all().order_by('-id')
    bid_nav = Bidang.objects.all()

    #search 
    search_query = request.GET.get('cari')
    if search_query:
        data = data.filter(
            Q(nama__icontains=search_query) |
            Q(nim__icontains=search_query) |
            Q(alamat__icontains=search_query) |
            Q(diverifikasi__icontains=search_query)
        )

    # pagination
    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'datas': page_obj,
        'bid_nav': bid_nav,
        'search_query': search_query
    }

    if request.method == 'POST':
        anggota_id = request.POST.get('anggota_id')
        anggota = Anggota.objects.get(id=anggota_id)
        anggota.diverifikasi = not anggota.diverifikasi
        anggota.save()

    return render(request, 'anggota.html', context)

@login_required()
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

@login_required()
@csrf_exempt
def anggota_detail(request,id):
    bid_nav = Bidang.objects.all()
    anggota = get_object_or_404(Anggota, id=id)

    context = {
        'anggota': anggota,
        'bid_nav': bid_nav,
    }
    return render(request,'anggota_detail.html',context)
@login_required()
@csrf_exempt
def anggota_delete(request,id):
    anggota = get_object_or_404(Anggota, id=id)
    anggota.delete()
    return redirect('dashboard:anggota')

#bidang
@login_required()
def bidang_list(request):
    bid_nav = Bidang.objects.all()
    context = {
        'bid_nav': bid_nav,
        }
    return render(request, 'snippets/navbar.html',context )
@login_required()
def bidang(request):
    bid_nav = Bidang.objects.all()
    search_query = request.GET.get('cari')

    if search_query:
        bid_nav = Bidang.objects.filter(nama_bidang__icontains=search_query)
    else:
        bid_nav = Bidang.objects.all()

    paginator = Paginator(bid_nav, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'bidang': page_obj,
        'bid_nav':bid_nav,
    }
    return render(request, 'bidang.html', context)
@login_required()
@csrf_exempt
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
@login_required()
@csrf_exempt
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
@login_required()
@csrf_exempt
def bidang_delete(request,id):
    bidang = get_object_or_404(Bidang, id=id)
    bidang.delete()
    return redirect('dashboard:bidang_list')

# pengurus
@login_required()  
def pengurus_list(request, id):
    bid_nav = Bidang.objects.all()
    bidangs = get_object_or_404(Bidang, id=id)
    pengurus = bidangs.bidang.all()

    query = request.GET.get('cari')
    if query:
        pengurus = pengurus.filter(
            Q(nama_pengurus__icontains=query) | Q(status__icontains=query)
        )

    paginator = Paginator(pengurus,5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'bidangs': bidangs, 
        'bid_nav': bid_nav, 
        'pengurus': page_obj, 
        'query': query 
    }

    return render(request, 'pengurus.html', context)
@login_required()
@csrf_exempt
def pengurus_create(request):
    bid_nav = Bidang.objects.all()
    if request.method == 'POST':
        form = PengurusForm(request.POST)
        if form.is_valid():
            pengurus = form.save()
            messages.success(request, "Data Berhasil di Tambah!")
            return redirect('dashboard:pengurus', id=pengurus.bidang.id)
    else:
        form = PengurusForm()

    context = {
        'form': form,
        'bid_nav': bid_nav,
    }
    return render(request, 'pengurus_crate.html',context)
@login_required()
@csrf_exempt
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
@login_required()
@csrf_exempt
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
            return redirect('dashboard:program_list') 
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

def calendar_view(request):
    events = Event.objects.all()
    bid_nav = Bidang.objects.all()
    context =  {
        'bid_nav':bid_nav,
        'events': events,
    }
    return render(request, 'program_calendar.html',context)

def all_events(request):                                                                                                 
    all_events = Event.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.title,                                                                                                                                                                                       
            'start': event.start_date.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end_date.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 

@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        event = Event(title=title, start_date=start_date, end_date=end_date)
        event.save()

        return redirect('dashboard:program_calendar')

# @csrf_exempt
# def update_event(request):
#     if request.method == 'POST':
#         event_id = request.POST['id']
#         start_date = request.POST['start_date']
#         end_date = request.POST['end_date']

#         event = Event.objects.get(id=event_id)
#         event.start_date = start_date
#         event.end_date = end_date
#         event.save()

#         return JsonResponse({'status': 'success'})

# @csrf_exempt
# def delete_event(request):
#     if request.method == 'POST':
#         event_id = request.POST['id']

#         event = Event.objects.get(id=event_id)
#         event.delete()

#         return JsonResponse({'status': 'success'})