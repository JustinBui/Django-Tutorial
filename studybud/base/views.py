from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic
from .forms import RoomForm
# from django.http import HttpResponse


# Create your views here.

# rooms = [
#     {'id':1, 'name':'Lets learn Python!'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Data scientists!'},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        # If user is logged in, they are not allowed to be on login page
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password').lower()
        
        try:
            user = User.objects.get(username=username) # IF the username exists
        except:
            messages.error(request, 'User does not exist') # Throw an error if user does not exist

        # User does exist, so therefore we authenticate their credentials:
        user = authenticate(request, username=username, password=password)

        # Seeing of user credentials were correct
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request) # Deleting session token, therefore logging user out
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Creating our user. However, we are freezing this operation
            # in time to access the user right away (Hence commit=False)
            user = form.save(commit=False)
            user.username = user.username.lower() # Updating username to lowercase form
            user.save() # Save the user onto database
            login(request, user) # Login user
            return redirect('home') # Redirect home
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form':form })

def home(request):
    # Retrieve GET request and find its query
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # Getting the topic specifically by __name... 
    # __icontains means if the query at least contains the same letters as exact search parameter (Ex: 'Py' is contained in search parameter 'Python') 
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | # Searchinig by topic name
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    # rooms = Room.objects.all() # Query all rooms in the database

    room_count = rooms.count() # We can also do len(rooms), but the count() method for query sets just work faster
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count}

    return render(request, 
                'base/home.html', # Render HTML page
                context) # Passing in rooms array into home.html as our CONTEXT into the HTML page

def room(request, pk):
    room = Room.objects.get(id=pk) # Getting 1 item based on a uid

    context = {'room': room}

    return render(request, 'base/room.html', context)

# The @ is a decorator: If the user is NOT logged in, they cannot create/update/delete rooms
# therefore, they get redirected to the login page
@login_required(login_url='login') 
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid(): # If it is valid data
            form.save()
            return redirect('home') # Redirect users back to the home page

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login') 
def updateRoom(request, pk): # Passing in primary key (pk) to know what item we are updating
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # Specifying instance=room to make a prefilled room

    # If the user is not the host of the room, they cannot update this room
    if request.user != room.host:
        return HttpResponse('You are not allowed here boy!')

    if request.method == 'POST': # Assumes user edits the form and submits it (Hence making a POST request)
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login') 
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # Only the host of the room is allowed to delete
    if request.user != room.host:
        return HttpResponse('You are not allowed here boy!')
    
    if request.method == 'POST': # Confirm to delete the room
        room.delete() # Remove that item from the database
        return redirect('home')
        
    return render(request, 'base/delete.html', {'obj':room})