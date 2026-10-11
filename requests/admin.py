from django.contrib import admin
from .models import Request, Review

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'tutor', 'date', 'is_processed')
    list_filter = ('subject', 'is_processed')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'tutor', 'rating', 'created_at')
    list_filter = ('rating',)