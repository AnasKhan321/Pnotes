from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from .models import Note
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/login")
def index(request):
    return render(request, 'index.html')


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        print(username, firstName, lastName, email, pass1, pass2)

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters ")
            return redirect('/')

        if not username.isalnum():
            messages.error(request, "Username must only contain letter and characters  ")
            return redirect('/')

        if len(pass1) < 8:
            messages.error(request, "Password is too small ")
            return redirect('/')

        if pass1 != pass2:
            messages.error(request, "Password does not match ")
            return redirect('/')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstName
        myuser.last_name = lastName
        myuser.save()
        messages.success(request, "Your icoder  account has been successfull created ")
        return redirect('/')
    else:
        return render(request, "signup.html")


def handleLogin(request):
    if request.method == 'POST':
        username = request.POST['loginusername']
        password = request.POST['loginpass']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "succesfully Logged In ")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password  ")
            return redirect('/')
    else:
        return render(request, 'Login.html')


def handleLogout(request):
    logout(request)
    return redirect('/')

def handledNotes(request):
    if request.method == 'POST':
        Nt = request.POST['title']
        Nd = request.POST['desc']
        user = request.user
        N = Note(user=user, Note_title=Nt, Note_Description=Nd)
        N.save()
        return  redirect('/mynote')

    else:
        print(request.user)
        return redirect('/')

@login_required(login_url="/login")
def fetchnote(request):
    Notes = Note.objects.filter(user=request.user)

    return  render(request,'mynote.html' ,{'Notes':Notes})

def search(request):
    if request.method == 'POST':
        query = request.POST['search']
        Notes = Note.objects.filter(Note_title__icontains=query)
        return render(request, 'mynote.html', {'Notes': Notes,'Message' : f"Search Result of Query :  {query}"})
def delete(request,id):
    Notes = Note.objects.get(id=id)
    Notes.delete()
    return  redirect('/mynote')

def UpdateNote(request,id):
    print(id)
    Notes = Note.objects.get(id=id)
    Notes.Note_title = request.POST['head']
    Notes.Note_Description = request.POST['head_t']
    Notes.save()
    return  redirect('/mynote')