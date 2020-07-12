from .models import Note
from django.forms import ModelForm


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'memo', 'important']

