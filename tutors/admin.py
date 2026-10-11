from django.contrib import admin
from .models import Tutor

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'experience', 'price', 'is_active')
    list_filter = ('subject', 'is_active')