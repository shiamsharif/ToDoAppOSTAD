from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ToDo
from .forms import ToDoForm

def todo_list(request):
    status_filter = request.GET.get('status', 'all')
    category_filter = request.GET.get('category', 'all')
    tasks = ToDo.objects.filter(user=request.user)

    if status_filter != 'all':
        tasks = tasks.filter(is_completed=(status_filter == 'completed'))

    if category_filter != 'all':
        tasks = tasks.filter(category=category_filter)
        
    complted_tasks = tasks.filter(is_completed=True)
    pending_tasks = tasks.filter(is_completed=False)
    
    return render(request, 'todo/todo_list.html', {
        'tasks': tasks,
        'completed_tasks': complted_tasks,
        'pending_tasks': pending_tasks,
        'status_filter': status_filter,
        'category_filter': category_filter,
    })
