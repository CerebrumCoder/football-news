# Dibuat untuk membuat struktur form yang dapat menerima data News baru.

from django.forms import ModelForm
from main.models import News

# Untuk menutup celah keamanan ini, kita akan melakukan 
# sanitasi data di sisi backend sebelum menyimpannya ke database. 
# Django menyediakan fungsi strip_tags yang sangat berguna untuk 
# menghapus semua tag HTML dari teks.
from django.utils.html import strip_tags

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'thumbnail', 'is_featured']
    
    # Method clean_title dan clean_content akan dipanggil secara otomatis saat 
    # form.is_valid() dijalankan. Dengan menambahkan kedua method ini, kamu 
    # memastikan bahwa semua data yang dikirim melalui NewsForm (misalnya di 
    # halaman create_news dan edit_news) sudah "bersih" dari tag HTML berbahaya 
    # sebelum disimpan.
    def clean_title(self):
        title = self.cleaned_data["title"]
        return strip_tags(title)

    def clean_content(self):
        content = self.cleaned_data["content"]
        return strip_tags(content)