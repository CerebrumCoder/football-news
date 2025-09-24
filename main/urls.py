from django.urls import path
from main.views import (show_main, 
                        create_news, show_news, show_xml, 
                        show_json, show_json_by_id, show_xml_by_id, 
                        register, login_user, logout_user, show_index, edit_news,
                        delete_news)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-news/', create_news, name='create_news'),
    path('news/<str:id>/', show_news, name='show_news'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:news_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:news_id>/', show_json_by_id, name='show_json_by_id'),

    # Untuk authentikasi user registrasi dan login
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # Untuk edit news yang ada
    path('news/<uuid:id>/edit/', edit_news, name='edit_news'),
    # Untuk delete news yang ada
    path('news/<uuid:id>/delete', delete_news, name='delete_news'),

    # Coba2 buat latihan saja
    path('index/', show_index, name='show_index'),
]