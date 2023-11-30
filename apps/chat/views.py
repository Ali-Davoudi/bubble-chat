from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Room

from apps.account.models import User
from apps.account.forms import AddUserForm, EditUserForm


@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')

    Room.objects.create(uuid=uuid, client=name, url=url)
    return JsonResponse({'message': 'room created'})


@login_required
def chat_admin(request):
    rooms = Room.objects.all()
    users = User.objects.filter(is_staff=True)

    context = {'rooms': rooms, 'users': users}
    return render(request, 'chat/chat_admin.html', context)


@login_required
def room(request, uuid):
    room = Room.objects.get(uuid=uuid)

    if room.status == Room.WAITING:
        room.status = Room.ACTIVE
        room.agent = request.user
        room.save()

    context = {'room': room}
    return render(request, 'chat/room.html', context)


@login_required
def delete_room(request, uuid):
    # This is an access for user permissions, can set deleteing, adding and etc for specific action
    if request.user.has_perm('room.delete_room'):
        room = Room.objects.get(uuid=uuid)
        room.delete()

        messages.success(request, 'The room was deleted!')
        return redirect('/chat-admin')
    else:
        messages.error(request, "You don't have access to delete rooms!")
        return redirect('/chat-admin')


@login_required
def add_user(request):
    if request.user.has_perm('user.add_user'):
        if request.method == 'POST':
            form = AddUserForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                user.is_staff = True
                user.set_password(request.POST.get('password'))
                user.save()

                if user.role == User.MANAGER:
                    group = Group.objects.get(name='Managers')
                    group.user_set.add(user)

                messages.success(request, 'The user was added!')
                return redirect('/chat-admin')

        else:
            form = AddUserForm()

        context = {'form': form}
        return render(request, 'chat/add_user.html', context)

    else:
        messages.error(request, "You don't have access to add users!")
        return redirect('/chat-admin')


@login_required
def user_detail(request, uuid):
    user = User.objects.get(pk=uuid)

    context = {
        'user': user,
        'rooms': user.rooms.all()  # related name is room in models
    }

    return render(request, 'chat/user_detail.html', context)


@login_required
def edit_user(request, uuid):
    if request.user.has_perm('edit_user'):
        user = User.objects.get(pk=uuid)

        if request.method == 'POST':
            form = EditUserForm(request.POST, instance=user)

            if form.is_valid():
                form.save()

                messages.success(request, 'The changes was saved!')
                return redirect('/chat-admin')

        else:
            form = EditUserForm(instance=user)

        context = {'user': user, 'form': form}
        return render(request, 'chat/edit_user.html', context)

    else:
        messages.error(request, "You don't have access to edit users!")
        return redirect('/chat-admin')
