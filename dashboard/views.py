from multiprocessing import context
from pickle import FALSE
from unittest import result
from urllib import request, response
from django.shortcuts import render, redirect
from .models import Notes, Homework, Todo
from .forms import ConversionForm, ConversionLengthForm, ConversionMassForm, DashboardForm, NotesForm, HomeworkForm, TodoForm, UserReg
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import DashboardForm
from wikipedia.exceptions import DisambiguationError



# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')

@login_required(redirect_field_name='login')
def notes(request):
    
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = form.save(commit=False)
            notes.user = request.user
            notes.save()

        messages.success(request, f'Notes Added from {request.user.username} Successfully')
        return redirect('notes')

    else:
        form = NotesForm()
        
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}

    return render(request, 'dashboard/notes.html', context)

def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

class details_note(generic.DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'

@login_required(redirect_field_name='login')
def homework(request):
    homeworks = Homework.objects.filter(user=request.user)
    done = None
    if len(homeworks) == 0:
        done = True

    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            # try:
            #     finished = request.POST['is_finished']
            #     if finished == 'on':
            #         finished = True
            #     else:
            #         finished = False
            # except:
            #     finished = False

            homework_form = form.save(commit=False)
            homework_form.user = request.user
            # homework_form.is_finished = finished
            homework_form.save()
            messages.success(request, f'Homework Added from {request.user.username} Successfully')
            return redirect('homework')
    else:
        form = HomeworkForm()
    
    context = {'homeworks': homeworks, 'done': done, 'form': form}
    return render(request, 'dashboard/homework.html', context)

def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

def update_homework(request, pk):
    homework = Homework.objects.get(id=pk)
    
    if homework.is_finished == True:
        homework.is_finished = False
    elif homework.is_finished == False:
        homework.is_finished = True
    homework.save()

    return redirect('homework')

@login_required(redirect_field_name='login')
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']

            result_dict['description'] = desc
            result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list
            }
        
        return render(request, 'dashboard/youtube.html', context)

    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)

@login_required(redirect_field_name='login')
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, f'Todo Added from {request.user.username} Successfully')
            return redirect('todo')
    else:
        form = TodoForm()    
    todos = Todo.objects.filter(user=request.user)
    context = {'todos': todos, 'form': form}
    return render(request, 'dashboard/todo.html', context)

def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

def update_todo(request, pk=None):
    homework = Todo.objects.get(id=pk)
    
    if homework.is_finished == True:
        homework.is_finished = False
    elif homework.is_finished == False:
        homework.is_finished = True
    homework.save()

    return redirect('todo')

@login_required(redirect_field_name='login')
def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q='+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('infoLink')
            }

            result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list
            }
        
        return render(request, 'dashboard/youtube.html', context)

    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/books.html', context)

@login_required(redirect_field_name='login')
def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/'+text
        r = requests.get(url)
        answer = r.json()
        
        phonetics = answer[0]['phonetics'][0]['text']
        audio = answer[0]['phonetics'][0]['audio']
        definition = answer[0]['meanings'][0]['definitions'][0]['definition']
        # example = answer[0]['meanings'][0]['definitions'][0]['example']
        synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
        context = {
            'form': form,
            'input':text,
            'phonetics':phonetics,
            'audio':audio,
            'definition': definition,
            # 'example': example,
            'synonyms': synonyms
        }
        
        
        # context = {
        #     'form': form,
        #     'input':''
        # }
 
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    
    return render(request, 'dashboard/dictionary.html', context)

@login_required(redirect_field_name='login')
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        
        try:
            search = wikipedia.page(text)
            context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'details': search.summary
            }
            return render(request, 'dashboard/wiki.html', context)
        except DisambiguationError as e:
            options = e.options
            context = {
                'form': form,
                'options': options,
                'error_message': f'The term "{text}" is ambiguous. Please choose one of the following:'
            }
            return render(request, 'dashboard/wiki_disambiguation.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/wiki.html', context)

@login_required(redirect_field_name='login')
def conv(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurment_form = ConversionLengthForm()
            context = {'form':form, 'm_form':measurment_form, 'input':True}
            
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''

                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form': form,
                    'm_form': measurment_form,
                    'input': True,
                    'answer':answer
                }

        
        if request.POST['measurement'] == 'mass':
            measurment_form = ConversionMassForm()
            context = {'form':form, 'm_form':measurment_form, 'input':True}
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''

                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilograms'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)/0.453592} pounds'
                context = {
                    'form': form,
                    'm_form': measurment_form,
                    'input': True,
                    'answer':answer
                } 

    else:
        form = ConversionForm()
        context = {'form': form, 'input':False}
    return render(request, 'dashboard/conversion.html', context)

def user_reg(request):
    form = UserReg()
    if request.method == 'POST':
        form = UserReg(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data('username')
            messages.success(request, f'account created for user: {username}')
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'dashboard/register.html', context)

def log_out(request):
    logout(request)
    return render(request, 'registration/logout.html')

def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
        
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False

    context = {
        'homeworks': homeworks,
        'todos': todos,
        'h_done': homework_done,
        't_done': todos_done
    }

    return render(request, 'dashboard/profile.html', context)
