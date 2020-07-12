from django.contrib import admin
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Note, NoteAdmin)

