from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.db.models import Q
from .models import Topic
from .forms import TopicForm

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    # User logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        if username != 'Justin_Bui':
            username = username.lower()

        password = request.POST.get('password')

        print(f'username: {username}, password: {password}')
        print('All users', User.objects.all())
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        print('What is user', user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password')

    page = 'login'
    context = {'page':page}
    return render(request, 'forum/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration.')

    context = {'form': form}
    return render(request, 'forum/login_register.html', context)


# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # topics = Topic.objects.all()
    topics = Topic.objects.filter(
        Q(title__icontains=q) |
        Q(creator__username__icontains=q)
    )

    context = {'topics': topics}
    return render(request, 'forum/home.html', context)


def topics(request, pk): # Getting a specific topic (Based on primary key)
    topic = Topic.objects.get(id=pk)
    topic_messages = topic.message_set.all()
    context = {'topic': topic, 'topic_messages':topic_messages}
    
    return render(request, 'forum/topic.html', context)


# ---------- CRUD ---------- 
@login_required(login_url='login') # Redirect to login page if not logged in already
def create_topic(request): # Rendering a form
    form =  TopicForm()
    context = {'form': form} # User renders form page

    # User submits a form 
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    
    return render(request, 'forum/create-topic.html', context)

@login_required(login_url='login')
def update_topic(request, pk):
    topic = Topic.objects.get(id=pk)
    form = TopicForm(instance=topic)

    if request.user != topic.creator:
        return HttpResponse('You do not have permission to update this topic')

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'forum/create-topic.html', context)

@login_required(login_url='login')
def delete_topic(request, pk):
    topic = Topic.objects.get(id=pk)
    context = {'topic':topic}

    if request.user != topic.creator:
        return HttpResponse('You do not have permission to delete this topic')
    
    if request.method == 'POST':
        topic.delete()
        return redirect('home')

    return render(request, 'forum/delete-topic.html', context)