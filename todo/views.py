from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ToDo
from .forms import ToDoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

@login_required
def task_list(request):
    status_filter = request.GET.get('status', 'all')
    category_filter = request.GET.get('category', 'all')
    tasks = ToDo.objects.filter(user=request.user)

    if status_filter != 'all':
        tasks = tasks.filter(is_completed=(status_filter == 'completed'))

    if category_filter != 'all':
        tasks = tasks.filter(category=category_filter)
        
    complted_tasks = tasks.filter(is_completed=True)
    pending_tasks = tasks.filter(is_completed=False)
    
    return render(request, 'task_list.html', {
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
            return redirect('task_create')
    else:
        form = ToDoForm()
    return render(request, 'task_form.html', {'form': form})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(ToDo, pk=pk, user=request.user)
    messages.success(request, 'Task Detail view successfully!')
    return render(request, 'task_detail.html', {'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(ToDo, pk=pk, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')    
    return redirect('task_list')

@login_required
def task_make_completed(request, pk):
    task = get_object_or_404(ToDo, pk=pk, user=request.user)
    task.is_completed = True
    task.status = 'completed' # Update status to 'completed'
    task.save()
    messages.success(request, 'Task marked as completed!')
    return redirect('task_list')

#user registration and login
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully!')

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Correct field

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {username}!')
                return redirect('task_list')
            else:
                messages.error(request, "Authentication failed. Please log in manually.")
                return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})



# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, f'Welcome back {username}!')
#             return redirect('task_list')
#         else:
#             messages.error(request, 'Invalid username or password.')
#     return render(request, 'registration/login.html')