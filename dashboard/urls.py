from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('notes', notes, name='notes'),
    path('delete_notes/<int:pk>', delete_note, name='delete_note'),
    path('details_notes/<int:pk>', details_note.as_view(), name='details_note'),
    path('homework', homework, name='homework'),
    path('delete_homework/<int:pk>', delete_homework, name='delete_homework'),
    path('update_homework/<int:pk>', update_homework, name='update_homework'),
    path('youtube', youtube, name='youtube'),
    path('todo', todo, name='todo'),
    path('delete_todo/<int:pk>', delete_todo, name='delete_todo'),
    path('update_todo/<int:pk>', update_todo, name='update_todo'),
    path('books', books, name='books'),
    path('dictionary', dictionary, name='dictionary'),
    path('wiki', wiki, name='wiki'),
    path('conv', conv, name='conv'),
    path('profile', profile, name='profile'),
    path('logout/', log_out, name='logout'),
    
    
]
