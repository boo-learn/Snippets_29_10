from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "POST":
        # form_data = request.POST
        # snippet = Snippet(
        #     name=form_data['name'],
        #     lang=form_data['lang'],
        #     code=form_data['code']
        # )
        # snippet.save()
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('snippet-list')
    elif request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
    }
    return render(request, 'pages/view_snippets.html', context)
