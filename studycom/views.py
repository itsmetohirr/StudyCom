from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm


def login_view(request):
    invalid = False

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('user found')
            login(request, user)
            return redirect('home')
        else:
            invalid = True


    context = {'invalid': invalid}
    return render(request, 'studycom/login_page.html', context)


def register_user(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
            messages.error(request, 'An error occured during registration')

    context = {'form': form}
    return render(request, 'studycom/register_page.html', context)


def logout_view(request):
    logout(request)

    return redirect('home')


def home_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    topics = Topic.objects.all()[0:7]
    room_count = rooms.count()
    activity_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:7]

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'activity_messages': activity_messages}

    return render(request, 'studycom/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)

        message.save()
        return redirect('room', pk=room.id)


    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'studycom/room.html', context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    user_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'activity_messages': user_messages, 'topics': topics}
    return render(request, 'studycom/profile.html', context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
            
        return redirect('home')

    topics = Topic.objects.all()
    context = {'form': form, 'topics': topics}
    return render(request, 'studycom/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed to edit')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        
        return redirect('home')

    topics = Topic.objects.all()
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'studycom/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed to edit')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'studycom/delete.html', {'obj': room})


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to edit')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'studycom/delete.html', {'obj': message})


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        print(request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    
    return render(request, 'studycom/update-user.html', {'form': form})


# ---------- Mobil Responsiveness ------------ #

def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    
    return render(request, 'studycom/topics_mobile.html', {'topics': topics})


def activity(request):
    activity_messages = Message.objects.all()

    return render(request, 'studycom/activity_mobile.html', {'activity_messages': activity_messages})
