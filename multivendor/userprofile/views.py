from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Userprofile
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from store.forms import ProductForm


# Create your views here.

def vendor_details(request, pk):
    user = User.objects.get(pk = pk)
    context = {
        'user': user,
    }

    return render(request, 'userprofile/vendor_details.html', context)

@login_required
def my_store(request):
    return render(request, 'userprofile/my_store.html')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('title')
            product = form.save(commit = False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()

            return redirect('my_store')
        
    else:
        form = ProductForm()

    return render(request, 
                  'userprofile/add_product.html',
                  {
                      'form': form
                  })

@login_required
def myaccount(request):
    return render(request, 'userprofile/myaccount.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            userprofile = Userprofile.objects.create(user = user)

            return redirect('frontpage')

    else:
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'userprofile/signup.html', context)

        