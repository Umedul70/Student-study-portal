from typing import Generic
from django.contrib.auth.models import User
from django.core.checks import messages
from django.http import request
from django.shortcuts import redirect, render
from .models import Homework, Notes, Todo
from . forms import ConversinonLengthForm, ConversinonMassForm, ConversionForm, HomeworkForm, NotesForm, SearchForm, TodoForm, UserRegistrationForm
from django.contrib import messages
from django.views.generic.detail import DetailView
from youtubesearchpython import VideosSearch, search
from dashboard import forms
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    if request.method =="POST":
        form = NotesForm(request.POST)
        if form.is_valid:
            notes = Notes(user = request.user,title = request.POST['title'],description = request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added From {request.user.username} Sucessfully")
    else:
        form = NotesForm()
    form = NotesForm()
    notes = Notes.objects.filter(user = request.user)
    params = {'notes':notes,'form':form}
    return render(request,'dashboard/notes.html', params)


def delete_note(request, pk=None):
    Notes.objects.get(id = pk).delete()
    return redirect('notes')

class notesDetailView(DetailView):
    model = Notes

@login_required
def homework(request):
    if request.method == 'POST':
        form =HomeworkForm(request.POST)
        if form.is_valid :
            try:
                finished =request.POST['is_finished']
                if finished=='on':
                    finished = True
                else:
                    finished =False
            except:
                finished = False
            homework =Homework(user =request.user, subject =request.POST['subject'], title = request.POST['title'],description = request.POST['description'],due = request.POST['due'],is_finished = finished )
            homework.save()
        messages.success(request,f"Homework Added From {request.user.username} Sucessfully")
    form = HomeworkForm()
    homework = Homework.objects.filter(user = request.user)
    params = {'homeworks':homework, 'form':form}
    return render(request, 'dashboard/homework.html',params)


def updateHomework(request, pk):
    work = Homework.objects.get(id = pk)
    if work.is_finished == True:
        work.is_finished = False
    elif work.is_finished == False:
        work.is_finished = True
    work.save()
    return redirect('homework')

def deleteHomework(request, pk):
    homework = Homework.objects.get(id = pk).delete()
    return redirect('homework')

def youtube(request):
    if request.method == 'POST':
        form=SearchForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list =[]
        for i in video.result()['result']:
            result_dict = {
                'input' : text,
                'title' : i['title'],
                'duration' : i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc+= j['text']
            result_dict['description']= desc
            result_list.append(result_dict)
        params = {'form':form, 'results':result_list}
    else:
        form = SearchForm()
        params = {'form':form}
    return render(request, 'dashboard/youtube.html',params)

@login_required
def todo(request):
    form = TodoForm(request.POST)
    if request.method =='POST':
        if form.is_valid:
            try:
                completed = request.POST['is_completed']
                if completed=='on':
                    completed = True
                else:
                    completed =False
            except:
                completed = False

            todo = Todo(user = request.user,
            title = request.POST['title'],
            is_completed= completed)
            todo.save()
        messages.success(request,f"Todo Added From {request.user.username} Sucessfully")
    form = TodoForm()
    todo = Todo.objects.filter(user = request.user)
    params = {'todos':todo, 'form':form}
    return render(request, 'dashboard/todo.html',params)

def updateTodo(request, pk):
    work = Todo.objects.get(id = pk)
    if work.is_completed == True:
        work.is_completed = False
    elif work.is_completed == False:
        work.is_completed = True
    work.save()
    return redirect('todo')


def deleteTodo(request, pk):
    todo = Todo.objects.get(id = pk).delete()
    return redirect('todo')

def books(request):
    if request.method == 'POST':
        form=SearchForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list =[]
        for i in range(10):
            result_dict = {
                'title' : answer['items'][i]['volumeInfo']['title'],
                'subtitle' : answer['items'][i]['volumeInfo'].get('subtitle'),
                'desciption' : answer['items'][i]['volumeInfo'].get('description'),
                'count' : answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories' : answer['items'][i]['volumeInfo'].get('categories'),
                'rating' : answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail' : answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview' : answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
        params = {'form':form, 'results':result_list}
    else:
        form = SearchForm()
        params = {'form':form}
    return render(request, 'dashboard/books.html',params)

def dictionary(request):
    if request.method == 'POST':
        form=SearchForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definitions = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            params = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definitions':definitions,
                'example':example,
                'synonyms':synonyms
            }
        except:
            params={
                'form':form,
                'input':''
            }
        return render(request, 'dashboard/dictionary.html',params)
    else:
        form = SearchForm()
        params ={
            'form':form
        }
        return render(request, 'dashboard/dictionary.html',params)


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = SearchForm(request.POST)
        search = wikipedia.page(text)
        params = {
            'form':form,
            'title':search.title,
            'link': search.url,
            'details':search.summary
        }
        return render(request, 'dashboard/wiki.html',params)


    else:    
        form = SearchForm()
        params =  {
            'form':form
        }

        return render(request, 'dashboard/wiki.html',params)

def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurment']=='length':
            measurement_form =ConversinonLengthForm()
            params ={
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer =''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    elif first == 'foot' and second == 'yard':
                        answer = f'{input} yard = {int(input)/3} foot'
                params = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
        else:
            measurement_form =ConversinonMassForm()
            params ={
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer =''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    elif first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                params = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
    else:
        form = ConversionForm()
        params = {
            'form':form,
            'input':False
        }
    return render(request, 'dashboard/conversion.html', params)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid:
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created SucessFully For {username}")
            return redirect('login')
    else:
        form =UserRegistrationForm()
    params = {
        'form':form
    }
    return render(request, 'dashboard/register.html', params)

def profile(request):
    homework = Homework.objects.filter(is_finished =  False, user = request.user)
    todo = Todo.objects.filter(is_completed =  False, user = request.user)
    if len(homework)== 0:
        homework_done = True
    else:
        homework_done= False
    if len(todo)== 0 :
        todo_done = True
    else:
        todo_done = False
    params = {
        'homeworks':homework,
        'todos':todo,
        'homework_done':homework_done,
        'todo_done': todo_done
    }

    return render(request, 'dashboard/profile.html', params)
