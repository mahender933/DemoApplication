from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . forms import UserForm


@login_required(login_url='accounts:login')
def home(request):
    """
    Home View
    :param request:
    :return:
    """
    users_list = User.objects.all().order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(users_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_page)
    return render(request, 'accounts/home.html', {'users': users})


def sign_up(request):
    """
    New User Creation View
    :param request:
    :return:
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Successfully signed up !.")
            return redirect("accounts:home")
        else:
            messages.error(request, f"Unsuccessful Got Invalid Information ")
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        return render(request, 'accounts/signup.html', {'form': UserForm})


def logout_user(request):
    """
    Logout View
    :param request:
    :return:
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("accounts:home")


def login_user(request):
    """
    Login View
    :param request:
    :return:
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                messages.info(request, f"Successfully Logged in as {user}.")
                return redirect("accounts:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, f"Failed Login")
        return render(request=request, template_name="accounts/login.html", context={"form": form})
    else:
        form = AuthenticationForm()
        return render(request=request, template_name="accounts/login.html", context={"form": form})


@login_required(login_url='accounts:login')
def delete_user(request, pk: int):
    """
    Deletes a specific user from the database.
    :param request:
    :param pk: user object primary key
    :return:
    """
    try:
        u = User.objects.get(id=pk)
        u.delete()
        messages.success(request, "Successfully deleted the user")
    except User.DoesNotExist:
        messages.error(request, "User does not exist")
        return redirect("accounts:home")
    except Exception as e:
        messages.error(request, f"{e.__class__}")
    return redirect("accounts:home")
