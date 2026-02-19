from django.shortcuts import render, redirect
from .models import USER, TASK

# Create your views here.
def Login(request):
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        try:
            user = USER.objects.get(USERNAME=name, PASSWORD=password)
            return redirect(f'/app/{user.id}/')
        except:
            return render(request, 'login.html', {"error": "Invalid username or password"})
    return render(request, 'login.html')
# REGISTER
def Register(request):
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        USER.objects.create(USERNAME=name, PASSWORD=password)
        return redirect('/login/')
    return render(request, 'register.html')
# APP PAGE (ONLY NOT COMPLETED TASKS)
def App(request, user_id):
    user = USER.objects.get(id=user_id)
    # Pending tasks
    pending_tasks = TASK.objects.filter(user=user, completed=False)
    # Completed tasks count
    completed_count = TASK.objects.filter(user=user, completed=True).count()
    return render(request, 'app.html', {
        "user": user,
        "tasks": pending_tasks,
        "completed_count": completed_count,
        "pending_count": pending_tasks.count()
    })
# ADD TASK
def AddTask(request, user_id):
    user = USER.objects.get(id=user_id)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        completed = request.POST.get('completed')
        TASK.objects.create(
            user=user,
            title=title,
            description=description,
            completed=True if completed == "on" else False
        )
        return redirect(f'/app/{user_id}/')
    return render(request, 'addtask.html', {"user": user})
# EDIT TASK
def EditTask(request, task_id, user_id):
    task = TASK.objects.get(id=task_id)
    user = USER.objects.get(id=user_id)
    if request.method == "POST":
        task.title = request.POST['title']
        task.description = request.POST['description']
        if request.POST.get('completed') == "on":
            task.completed = True
        else:
            task.completed = False
        task.save()
        return redirect(f'/app/{user_id}/')
    return render(request, 'edittask.html', {
        "task": task,
        "user": user
    })
# DELETE TASK
def DeleteTask(request, task_id, user_id):
    TASK.objects.get(id=task_id).delete()
    return redirect(f'/app/{user_id}/')
