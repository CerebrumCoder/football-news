import uuid
from django.db import models
from django.utils import timezone

class News(models.Model):
    CATEGORY_CHOICES = [
        ('transfer', 'Transfer'),
        ('update', 'Update'),
        ('exclusive', 'Exclusive'),
        ('match', 'Match'),
        ('rumor', 'Rumor'),
        ('analysis', 'Analysis'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    thumbnail = models.URLField(blank=True, null=True)

    # news_views otomatis diisi dengan waktu saat objek dibuat pada forms.py
    news_views = models.PositiveIntegerField(default=0)
    # created_at otomatis diisi dengan waktu saat objek dibuat pada forms.py
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    @property
    def is_news_hot(self):
        return self.news_views > 20
        
    def increment_views(self):
        self.news_views += 1
        self.save()

    # def get_category_display(self):
    #     return dict(self.CATEGORY_CHOICES).get(self.category, 'Unknown')

class Person(models.Model):
    display_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=17, unique=True)
    
    def __str__(self):
        return self.display_name

class Post(models.Model):
    # ForeignKey untuk link to another model
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    content = models.CharField(max_length=125)
    published_date = models.DateTimeField(default=timezone.now)
