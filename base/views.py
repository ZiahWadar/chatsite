from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm



# Create your views here.

# rooms = [
#     {'id':1, 'name': 'lets learn python'},
#     {'id':2, 'name': 'Design withme'},
#     {'id':3, 'name': 'frontend developers'}
# ]


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(descriptions__icontains=q) |
        Q(name__icontains=q)
    )
    
    topics  = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(
        room__topic__name__icontains=q
    ))
    
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)




def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)


@login_required(login_url = 'login')
def createRoom(request):
    form = Room.objects.all()
    form = RoomForm
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('you are not allowed here!!!')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')
def delete_room(request, pk):
    
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    if request.user != room.host:
        return HttpResponse('you are not allowed here!!!')
    
    context = {'room':room}
    return render(request, 'base/delete.html', context)
 

def register(request):
    
    
    if request.user.is_authenticated:
        return redirect('home')
    
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'error occour during registration')
            
    
    context = {'form':form}
    return render(request, 'base/login_register.html', context)


def loginuser(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'wrong username or password')
    
    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutuser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def deleteMessage(request, pk):
    
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    context = {'room':room}
    return render(request, 'base/delete.html', context)


def userprofile(request, pk):
    user = User.objects.get(id=pk)
    context = {'user':user}
    return render(request, 'base/profile.html', context)



