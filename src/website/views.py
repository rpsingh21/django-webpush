from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model
)
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from webpush.models import PushInformation

from .forms import LoginForm, MessageForm
from .tasks import send_notification_to_user, send_notification_to_group
User = get_user_model()


@login_required(login_url='/login/')
def home(request):
    print(request)
    context = {
        'webpush': {"group": 'alluser'},
        'title': 'home'
    }
    return render(request, 'home.html', context)


@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_superuser)
def subscribed_user(request):
    instances = PushInformation.objects.all()
    context = {
        'title': 'all subscribe users',
        'instances': instances
    }
    return render(request, 'subscribeUser.html', context)


@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_superuser)
def send_notification(request):
    form = MessageForm(request.POST, None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            message = form.cleaned_data.get("message")
            if username == "alluser":
                send_notification_to_group(username, message)
            else:
                send_notification_to_user.delay(username, message)
            return JsonResponse({'status': 'true', 'message': 'successfuly'}, status=200)

    return JsonResponse({'status': 'false', 'message': 'bad request'}, status=504)


def login_view(request):
    form = LoginForm(request.POST or None)
    next = request.GET.get('next')
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect("/account")
    next = request.META.get('HTTP_REFERER')
    return render(request, "loginForm.html", {"title": "LOGIN", "form": form})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
