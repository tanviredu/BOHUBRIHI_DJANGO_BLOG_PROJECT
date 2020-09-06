from django.shortcuts import render
from .forms import SignupForm,UserProfileChange,ProfilePic
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required


def sign_up(request):
    form = SignupForm()
    registered = False 
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True
            return HttpResponseRedirect(reverse("index"))
    ctx = {'form':form,'registered':registered}
    return render(request,'App_Login/signup.html',ctx)

def login_page(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse("index"))
    return render(request,'App_Login/login.html',{'form':form})

@login_required
def profile(request):
    return render(request,'App_Login/profile.html')
    
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def user_change(request):
    current_user = request.user
    changed = False 
    form = UserProfileChange(instance=current_user)
    if request.method == "POST":
        form = UserProfileChange(request.POST,instance=current_user)
        if form.is_valid():
            form.save()
            changed = True
            ## reset the form
            form = UserProfileChange(instance=current_user)
            return HttpResponseRedirect(reverse("index"))
            ## but you cant change the password here
            ## thats an additional work
    return render(request,'App_Login/change_profile.html',{'form':form,'changed':changed})



@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == "POST":
        form = PasswordChangeForm(current_user,data=request.POST)
        if form.is_valid():
            form.save()
            changed =True
            return HttpResponseRedirect(reverse('index'))
    return render(request,'App_Login/pass_change.html',{'form':form,'changed':changed})


@login_required
def add_pro_pic(request):
    form = ProfilePic()
    if request.method == "POST":
        form = ProfilePic(request.POST,request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse("App_Login:profile"))
    return render(request,'App_Login/pro_pic_add.html',{'form':form})

@login_required
def change_pro_pic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == "POST":
        form = ProfilePic(request.POST,request.FILES,instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("App_Login:profile"))
    return render(request,'App_Login/pro_pic_add.html',{'form':form})