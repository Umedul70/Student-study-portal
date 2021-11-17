from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name = 'home'),
    path('notes',views.notes, name = 'notes'),
    path('delete_note/<int:pk>', views.delete_note, name = 'delete_note'),
    path('notes_detail/<int:pk>', views.notesDetailView.as_view(), name = 'notes-detail'),
    path('homework',views.homework, name='homework'),
    path('update_homework/<int:pk>',views.updateHomework, name='updateHomework'),
    path('delete_homework/<int:pk>', views.deleteHomework, name = 'delete_homework'),
    path('youtube',views.youtube, name='youtube'),
    path('todo',views.todo, name='todo'),
    path('update_todo/<int:pk>',views.updateTodo, name='updateTodo'),
    path('delete_todo/<int:pk>',views.deleteTodo, name='deleteTodo'),
    path('books',views.books, name='books'),
    path('dictionary',views.dictionary, name='dictionary'),
    path('wiki',views.wiki, name='wiki'),
    path('conversion',views.conversion, name='conversion'),
]
