from django.contrib import admin
from .models import ToDo
@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):  
    list_display = ('title', 'status', 'category', 'due_date', 'is_completed', 'user')
    list_filter = ('status', 'category', 'is_completed')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
# Register your models here.
