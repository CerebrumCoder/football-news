# Dibuat untuk membuat struktur form yang dapat menerima data News baru.

from django.forms import ModelForm
from main.models import News

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'thumbnail', 'is_featured']