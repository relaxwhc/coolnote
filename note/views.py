from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone

from .models import Note
from .forms import NoteForm


def home(request):
    return render(request, 'home.html')


def signup_user(request):
    if request.method == "GET":
        form = UserCreationForm
        return render(request, 'signupuser.html', {'form': form()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_note')
            except IntegrityError:
                return render(request, 'signupuser.html',
                              {'form': UserCreationForm(),
                               'error': 'The username is already taken.',
                               'error2': 'Please try another username.'})
        else:
            return render(request, 'signupuser.html',
                          {'form': UserCreationForm(),
                           'error': 'The passwords did not match.',
                           'error2': 'Please try again.'})


def login_user(request):
    if request.method == "GET":
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'The username or the password is wrong.',
                           'error2': 'Please try again.'})
        else:
            login(request, user)
            return redirect('current_note')


@login_required
def logout_user(request):
    if request.method == "GET":
        return redirect('current_note')
    else:
        logout(request)
        return redirect('home')


@login_required
def current_note(request):
    notes = Note.objects.filter(user=request.user, datecompleted__isnull=True).\
        order_by('-created')
    return render(request, 'currentnote.html', {'notes': notes})


# LIST OF ITEMS MARKED COMPLETED
@login_required
def completed_note(request):
    notes = Note.objects.filter(user=request.user, datecompleted__isnull=False).\
        order_by('-datecompleted')
    return render(request, 'completednote.html', {'notes': notes})


@login_required
def create_note(request):
    if request.method == "GET":
        return render(request, 'createnote.html', {'form': NoteForm()})
    else:
        try:
            form = NoteForm(request.POST)
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            return redirect('current_note')
        except ValueError:
            return render(request, 'createnote.html',
                          {'form': NoteForm(),
                           'error': 'Bad data passed in.',
                           'error2': 'Please try again.'})


@login_required
def view_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk, user=request.user)
    if request.method == 'GET':
        form = NoteForm(instance=note)
        return render(request, 'viewnote.html', {'note': note, 'form': form})
    else:
        try:
            form = NoteForm(request.POST, instance=note)
            form.save()
            return redirect('current_note')
        except ValueError:
            return render(request, 'viewnote.html',
                          {'note': note, 'form': NoteForm(),
                           'error': 'Bad data passed in.',
                           'error2': 'Please try again'})


# MARK ITEM AS COMPLETE
@login_required
def complete_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk, user=request.user)
    if request.method == 'POST':
        note.datecompleted = timezone.now()
        note.save()
        return redirect('current_note')
    else:
        return redirect('current_note')


@login_required
def delete_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('current_note')
    else:
        return redirect('current_note')
