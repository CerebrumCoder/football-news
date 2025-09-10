# HttpResponse merupakan class yang digunakan 
# untuk menyusun respon yang ingin dikembalikan oleh server ke user
from django.http import HttpResponse

# serializers digunakan untuk translate objek model menjadi format lain seperti dalam fungsi ini adalah XML
from django.core import serializers

from django.shortcuts import render, redirect, get_object_or_404
from main.forms import NewsForm
from main.models import News
# from .models import Person, Post

def show_main(request):
    # Ditambahkan untuk mengambil seluruh objek News yang tersimpan pada database
    news_list = News.objects.all()

    context = {
        'npm' : '2406348282',
        'name': 'Neal Guarddin',
        'class': 'PBP A',
        'news_list': news_list,
    }

    return render(request, "main.html", context)

# Method baru untuk menghasilkan form yang dapat menambahkan data News secara 
# otomatis ketika data di-submit dari form
def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')
    
    context = {'form': form}
    return render(request, 'create_news.html', context)

# Method show_news menggunakan get_object_or_404(News, pk=id) untuk mengambil 
# objek News berdasarkan primary key (id). Jika objek tidak ditemukan, akan mengembalikan halaman 404.
def show_news(request, id):
    news = get_object_or_404(News, pk=id)

    # Digunakan untuk menambah jumlah views pada berita tersebut
    news.increment_views()

    context = {
        'news': news
    }

    return render(request, 'news_detail.html', context)

# Untuk mengembalikan Data dalam Bentuk XML
def show_xml(request):
    news_list = News.objects.all()
    xml_data = serializers.serialize("xml", news_list)
    return HttpResponse(xml_data, content_type="application/xml")

# Untuk mengembalikan Data dalam Bentuk JSON
def show_json(request):
    news_list = News.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")

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
        news_item = News.objects.filter(pk=news_id)
        json_data = serializers.serialize("json", [news_item])
        return HttpResponse(json_data, content_type="application/json")
    except News.DoesNotExist:
        return HttpResponse(status=404)
