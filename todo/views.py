from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ToDo
from .forms import ToDoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

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


@login_required
def task_create(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Task created successfully!')
            return redirect('todo_list')
    else:
        form = ToDoForm()
    return render(request, 'todo/task_form.html', {'form': form})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(ToDo, pk=pk, user=request.user)
    messages.success(request, 'Task Detail view successfully!')
    return render(request, 'todo/task_detail.html', {'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(ToDo, pk=pk, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')    
    return redirect('todo_list')

@login_required
def task_make_completed(request, pk):
    task = get_object_or_404(ToDo, pk=pk, user=request.user)
    task.is_completed = True
    task.save()
    messages.success(request, 'Task marked as completed!')
    return redirect('todo_list')

#user registration and login
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if  form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully!')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome {username}!')
            return redirect('todo_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})