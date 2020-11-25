from django.shortcuts import render, redirect
from .forms import PythonCreateForm
from .models import Python


def index(req):
    pythons = Python.objects.all()
    return render(req, 'index.html', {'pythons': pythons})


def create(req):
    if req.method == 'GET':
        form = PythonCreateForm()
        forms = {
            'normalform': form,
        }
        return render(req, 'create.html', forms)
    else:
        data = req.POST
        form = PythonCreateForm(data)
        if form.is_valid():
            python = form.save()
            python.save()
            return redirect('index')
