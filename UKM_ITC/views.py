from django.shortcuts import render,redirect, get_object_or_404
from ITC_APP . models import Anggota
from ITC_APP. forms import AnggotaForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login,logout


@csrf_exempt
def index(request):

    context = {}
    return render(request,'index.html',context)

@csrf_exempt
def form_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request,"Selamat, Login Berhasil!")
            return redirect('dashboard:dashboard') 
        else:
            return redirect('form_login')

    return render(request, 'form_login.html')
    
@csrf_exempt
def form_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('form_login')

@csrf_exempt
def sukses_home(request):
    return render(request, 'sukses_home.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = AnggotaForm(request.POST)
        if form.is_valid():
            anggota = form.save()
            return redirect('sukses')
    else:
        form = AnggotaForm()
    return render(request, 'form_anggota.html', {'form': form})