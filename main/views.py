
# Untuk menggunakan Data Dari Cookies
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

# Untuk merestriksi akses halaman Main dan News Detail
from django.contrib.auth.decorators import login_required

# import UserCreationForm dan messages untuk kepentingan registrasi user
# UserCreationForm adalah impor formulir bawaan yang memudahkan pembuatan 
# formulir pendaftaran pengguna dalam aplikasi web. Dengan formulir ini, 
# pengguna baru dapat mendaftar dengan mudah di situs web Anda tanpa harus 
# menulis kode dari awal
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# HttpResponse merupakan class yang digunakan 
# untuk menyusun respon yang ingin dikembalikan oleh server ke user
from django.http import HttpResponse

# serializers digunakan untuk translate objek model menjadi format lain seperti dalam fungsi ini adalah XML
from django.core import serializers

from django.shortcuts import render, redirect, get_object_or_404
from main.forms import NewsForm
from main.models import News
# from .models import Person, Post

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Untuk menutup celah keamanan ini, kita akan melakukan 
# sanitasi data di sisi backend sebelum menyimpannya ke database. 
# Django menyediakan fungsi strip_tags yang sangat berguna untuk 
# menghapus semua tag HTML dari teks.
from django.utils.html import strip_tags

# Mengaplikasikan decorator login_required untuk fungsi show_main dan show_news, 
# sehingga halaman utama dan news detail hanya dapat diakses oleh pengguna yang sudah login (terautentikasi).
@login_required(login_url='/login')
def show_main(request):
    # Ditambahkan untuk mengambil seluruh objek News yang tersimpan pada database dengan pemfilteran dulu
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        news_list = News.objects.all()
    else:
        news_list = News.objects.filter(user=request.user)

    context = {
        'npm' : '2406348282',
        'name': request.user.username,
        'class': 'PBP A',
        'news_list': news_list,
        # Untuk mengakses cookie yang terdaftar di request dengan request.COOKIES.get('last_login', 'Never')
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }

    return render(request, "main.html", context)

# Method baru untuk menghasilkan form yang dapat menambahkan data News secara 
# otomatis ketika data di-submit dari form
def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        news_entry = form.save(commit=False)
        news_entry.user = request.user  # Mengaitkan berita dengan pengguna yang sedang login
        news_entry.save()
        
        return redirect('main:show_main')
    
    context = {'form': form}
    return render(request, 'create_news.html', context)

# Method show_news menggunakan get_object_or_404(News, pk=id) untuk mengambil 
# objek News berdasarkan primary key (id). Jika objek tidak ditemukan, akan mengembalikan halaman 404.
# Mengaplikasikan decorator login_required untuk fungsi show_main dan show_news, 
# sehingga halaman utama dan news detail hanya dapat diakses oleh pengguna yang sudah login (terautentikasi).
@login_required(login_url='/login')
def show_news(request, id):
    news = get_object_or_404(News, pk=id)

    # Digunakan untuk menambah jumlah views pada berita tersebut
    news.increment_views()

    context = {
        'news': news
    }

    return render(request, 'news_detail.html', context)

# Fungsi untuk authentikasi user/pengguna yang ingin register
def register(request):
    # Digunakan untuk membuat UserCreationForm baru dari yang sudah diimpor sebelumnya
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been succesfully created!')
            
            # Nanti diarahkan ke laman login
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)

# Fungsi ini untuk mengautentikasi pengguna yang ingin login
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data =request.POST)

        # Tadi ini pake HTTPResponse, tapi diganti jadi HttpResponseRedirect 
        # dan reverse biar lebih rapi
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    
    context = {'form': form}
    return render(request, 'login.html', context)

# Fungsi ini untuk mengautentikasi pengguna yang ingin logout
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

# Fungsi untuk edit news pada aplikasi Django
# Menerima parameter request dan id 
# Lalu render halaman edit_news.html dengan context yang berisi form
def edit_news(request, id):
    news = get_object_or_404(News, pk=id)
    form = NewsForm(request.POST or None, instance=news)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')
    
    context = {
        'form': form,
    }

    return render(request, 'edit_news.html', context)

# Fungsi untuk menghapus news pada aplikasi
# Menerima parameter request dan id pada views.py untuk menghapus data news.
def delete_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

# Untuk mengembalikan Data dalam Bentuk XML
def show_xml(request):
    news_list = News.objects.all()
    xml_data = serializers.serialize("xml", news_list)
    return HttpResponse(xml_data, content_type="application/xml")

# Untuk mengembalikan Data dalam Bentuk JSON
def show_json(request):
    news_list = News.objects.all()
    data = [
        {
            'id': str(news.id),
            'title': news.title,
            'content': news.content,
            'category': news.category,
            'thumbnail': news.thumbnail,
            'news_views': news.news_views,
            'created_at': news.created_at.isoformat() if news.created_at else None,
            'is_featured': news.is_featured,
            'user_id': news.user_id,
        }
        for news in news_list
    ]
    # Parameter safe=False diperlukan karena data yang dikirim berupa list, bukan dictionary.
    return JsonResponse(data, safe=False)

# Untuk mengembalikan data berdasarkan ID dalam bentuk XML dan JSON

# Untuk mendapatkan data berdasarkan ID, kita dapat menggunakan berbagai 
# jenis method milik Django, dua di antaranya adalah filter() dan get(). 
# Namun, kedua method ini memiliki perbedaan yang cukup signifikan. filter() 
# dapat digunakan untuk mengambil data satu objek atau berbagai objek yang 
# memenuhi kondisi yang ditetapkan, sedangkan get() dapat digunakan untuk 
# mengambil data satu objek saja
def show_xml_by_id(request, news_id):
    try:
        news_item = News.objects.filter(pk=news_id)
        xml_data = serializers.serialize("xml", news_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except News.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, news_id):
    try:
        news = News.objects.select_related('user').get(pk=news_id)
        data = {
            'id': str(news.id),
            'title': news.title,
            'content': news.content,
            'category': news.category,
            'thumbnail': news.thumbnail,
            'news_views': news.news_views,
            'created_at': news.created_at.isoformat() if news.created_at else None,
            'is_featured': news.is_featured,
            'user_id': news.user_id,
            'user_username': news.user.username if news.user_id else None,
        }
        return JsonResponse(data)
    except News.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)


def show_index(request):
    context = {
        'nama': 'Neal',
    }
    return render(request, "index.html", context)

# @csrf_exempt: Menonaktifkan CSRF protection untuk request AJAX ini
# @require_POST: Memastikan hanya HTTP POST yang diterima
# == 'on': Handling khusus untuk checkbox (mengembalikan 'on' jika dicentang)
# Return HTTP response dengan status 201 (Created)
@csrf_exempt
@require_POST
def add_news_entry_ajax(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
    user = request.user

    new_news = News(
        title=title, 
        content=content,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_news.save()

    return HttpResponse(b"CREATED", status=201)

# Fungsi strip_tags akan menghilangkan semua tag HTML yang terdapat pada data 
# title dan content yang dikirim pengguna melalui POST request, sehingga data 
# yang disimpan dalam database adalah data yang sudah "bersih". Misal data = 
# "<b>Berita</b> <button>Penting</button> <span>Sekali</span>", maka strip_tags(data) 
# akan mengembalikan Berita Penting Sekali.

# Data lain seperti category, thumbnail, dan is_featured tidak perlu dibersihkan dengan 
# strip_tags karena tipe datanya sudah memberikan perlindungan yang kuat. Field category 
# dibatasi oleh choices, thumbnail divalidasi sebagai URL oleh URLField, dan is_featured 
# hanya menerima nilai boolean dari checkbox. Hal ini mencegah pengguna menyisipkan kode 
# HTML berbahaya pada field-field tersebut.
@csrf_exempt
@require_POST
def add_news_entry_ajax(request):
    title = strip_tags(request.POST.get("title")) # strip HTML tags!
    content = strip_tags(request.POST.get("content")) # strip HTML tags!