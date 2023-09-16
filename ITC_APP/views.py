from django.shortcuts import render,redirect, get_object_or_404
from .models import Anggota
from .forms import AnggotaForm

# Create your views here.
def home(request):
    return render(request,'home.html')
    
def index(request):
    return render(request,'index.html')

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

    context = {
        'datas':data,
    }
    return render(request,'anggota.html',context)

def anggota_detail(request,id):
    anggota = get_object_or_404(Anggota, id=id)

    context = {
        'anggota': anggota
    }
    return render(request,'anggota_detail.html',context)
