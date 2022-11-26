from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def index_page(request):
    print("user = ", request.user)
    if request.user.is_authenticated:
        errors = []
    else:
        errors = ["password or username not correct"]

    context = {
        'pagename': 'PythonBin',
        "errors": errors
    }

    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
        return redirect('snippet-list')
    elif request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    comment_form = CommentForm()
    comments = snippet.comments.all()
    context = {
        'pagename': 'Страница сниппета',
        "snippet": snippet,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, 'pages/snippet_page.html', context)


def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    snippet.delete()
    return redirect('snippet-list')


def snippets_page(request):
    snippets = Snippet.objects.all()

    lang = request.GET.get("lang")
    if lang is not None:
        snippets = snippets.filter(lang=lang)

    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'lang': lang
    }
    return render(request, 'pages/view_snippets.html', context)


@login_required()
def snippets_my(request):
    snippets = snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': snippets
    }
    return render(request, 'pages/view_snippets.html', context)



def comment_add(request):
   if request.method == "POST":
       comment_form = CommentForm(request.POST)
       snippet_id = request.POST['snippet_id']
       if comment_form.is_valid():
           comment = comment_form.save(commit=False)
           comment.author = request.user
           comment.snippet = Snippet.objects.get(id=snippet_id)
           comment.save()

       return redirect(f'/snippet/{snippet_id}')

   raise Http404




def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
    return redirect('home')


def logout_page(request):
    auth.logout(request)
    return redirect('home')


def registration(request):
    if request.method == "POST":  # Создаем пользователя
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = {'form': form}
            return render(request, 'pages/registration.html', context)
    elif request.method == "GET":  # Страницу с формой
        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, 'pages/registration.html', context)
