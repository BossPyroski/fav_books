from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from django.contrib import messages
from .models import *


def index(request):
    return render(request, "login.html")


def validate_login(request):
    user = User.objects.get(email=request.POST['email'])
    if bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode()):
        print("password match")
    else:
        print("failed password")


def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/main')
        request.session['userid'] = logged_user.id
        return redirect('/main')
    messages.error(request, "Invalid login")
    return redirect("/main")


def register(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        messages.error(request, "email is already in use", extra_tags="email")
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    this_user = User.objects.create(email=request.POST['email'], firstn=request.POST['firstn'], namesuf=request.POST['namesuf'], username=request.POST['username'], password=pw_hash)
    request.session['user_id'] = this_user.id
    return redirect("/")


def main(request):
    if "user_id" not in request.session:
        return redirect('/')
    context = {
        "books": Book.objects.all(),
        "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "main.html", context)

def logout(request):
    del request.session['user_id']
    return redirect('/')

def return_m(request):
    return redirect("/main")

def add_book(request):
    this_user = request.session['user_id']
    user = User.objects.get(id=this_user)
    this_book = Book.objects.create(
        title=request.POST['title'],
        description=request.POST['description'],
        uploaded_by=user
    )
    this_book.users_who_like.add(user)
    return redirect("/main")

def view_book(request, id):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "books": Book.objects.get(id=id)
    }
    return render(request, "view_book.html", context)

def destroy(request, id):
    deleteMe = Book.objects.get(id=id)
    deleteMe.delete()
    return redirect('/main')

def update(request, id):
    this_book = Book.objects.get(id=id)

    this_book.title=request.POST['title']
    this_book.description=request.POST['description']
    this_book.save()
    return redirect('/main')

def like(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    this_user = User.objects.get(id=request.session['user_id'])
    this_book = Book.objects.get(id=id)	
    if this_user in this_book.users_who_like.all():
        this_book.users_who_like.remove(this_user)
    else:
        this_book.users_who_like.add(this_user)
    return redirect('/main')