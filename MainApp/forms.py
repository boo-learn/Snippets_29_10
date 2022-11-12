from django.forms import ModelForm, Textarea, TextInput
from MainApp.models import Snippet


class SnippetForm(ModelForm):
   class Meta:
       model = Snippet
       # Описываем поля, которые будем заполнять в форме
       fields = ['name', 'lang', 'code']
       widgets = {
           'name': TextInput(attrs={"placeholder": "Название сниппета", "class": "blue"}),
           'code': Textarea(attrs={"placeholder": "Код сниппета"}),
       }
       labels = {
           'name': '',
           'lang': '',
           'code': ''
       }