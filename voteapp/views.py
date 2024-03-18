from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    categories = Category.objects.all()
    context = {'categories' : categories}
    return render(request, 'index.html', context)

@login_required(login_url='signin')
def detail(request, slug):
    category = Category.objects.get(slug=slug)
    categories = CategoryItem.objects.filter(category=category)

    if request.user.is_authenticated:
        if category.voters.filter(id=request.user.id).exists():
            messages.success(request, ' You Have Voted In This Category...')

    if request.method == "POST":
        selected_id = request.POST.get("category_item")
        print(selected_id)
        item = CategoryItem.objects.get(id=selected_id)
        item.total_vote += 1
        item_category = item.category
        item.category.total_vote += 1

        item.voters.add(request.user)
        item_category.voters.add(request.user)

        item.save()
        item_category.save()
        return redirect('result' , slug=category.slug)


    context = {'category' :  category, 'categories' :  categories}
    return render(request, 'detail.html', context)


def result(request, slug):
    category = Category.objects.get(slug=slug)
    items = CategoryItem.objects.filter(category=category)
    context = {'category' : category, 'items' : items}
    return render(request, 'result.html', context)


def signup(request):
    #this is to make user that have been logged in unable to go back to register since they have already being logged in
    if request.user.is_authenticated:
        return redirect('index')
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have registered successfully ')

            username = request.POST["username"]
            password = request.POST["password1"]

            #this is to get it in the database, we need to first import authenticate
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  #it generates a session for you, this enables the user to have access to the homepage
                messages.success(request, f"Dear {request.user}, you have Logged in successfully")
            return redirect('index')
        
    context = {'form' : form } #to access it on an html page using the key

    return render(request, 'signup.html', context)


def signin(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        #this is to get it in the database, we need to first import authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect('index')
           
        else:
            messages.error(request, 'Invalid Credentials')
    context = {}
    return render(request, 'signin.html', context)



def logoutView(request):
    logout(request)
    messages.success(request, " you have Logged out successfully")
    return render(request, 'logout.html')

