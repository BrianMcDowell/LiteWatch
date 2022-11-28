from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from .forms import NewSearchForm, UserRegisterForm
from .models import Search, Result
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from .mail import send_mail
from .cron import trigger

# Create your views here.


def index(request):

    # trigger()  # way to debug cron functionality.
    # Comment out or remove if not working on cron.

    if request.method == "POST":
        if 'changestate' in request.POST.keys():
            changesearchstate(request, request.POST['changestate'])
        elif 'deletesearch' in request.POST.keys():
            removesearch(request, request.POST['deletesearch'])
        elif 'deleteaccount' in request.POST.keys():
            check = deleteaccount(request, request.POST['usernamematch'])
            if not check:
                return render(request, 'useroptions.html', {'FailedDelete': True})
        else:
            form = NewSearchForm(request.POST or None)
            if not form.is_valid(): print(form.errors)
            if form.is_valid():
                the_form = form.save(commit=False)
                the_form.user_id = request.user.id
                the_form.save()
        return HttpResponseRedirect('/')

    if request.user.is_authenticated:
        context = {'userResultList': []}
        user_searches = Search.objects.filter(user_id=request.user.id)
        count = 0
        for item in user_searches:
            res = {
                'keyword': item.keyword,
                'url': item.url,
                'dateCreated': item.dateCreated,
                'hitIds': [],
                'state': "Enabled" if item.state else "Disabled",
                'id': item.id
                }
            search_results = Result.objects.filter(sourceSearch=item.id)
            res['hits'] = len(search_results)
            for result in search_results:
                res['hitIds'].append(result.id)
            context['userResultList'].append(res)
            count += 3

        return render(request, 'home.html', context)
    else:
        return render(request, 'externalhome.html', {})


def login(request):
    # https://learndjango.com/tutorials/django-login-and-logout-tutorial
    template = loader.get_template('registration/login.html')
    return HttpResponse(template.render())


def register(request):
    # https://www.krazyprogrammer.com/2021/01/django-user-registration-in-pycharm.html
    # https://www.geeksforgeeks.org/django-sign-up-and-login-with-confirmation-email-python/
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            return redirect('login')
            #template = loader.get_template('registration/login.html')
            # return HttpResponse(template.render())
            return render(request, 'registration.html', {'form': form, 'msg': "Registered Successfully"})
    else:
        form = UserRegisterForm()
    return render(request, 'registration.html', {'form': form})


def newsearch(request):
    form = NewSearchForm()
    return render(request, 'newsearch.html', {'form': form})


def removesearch(request, searchid):
    this_search = Search.objects.get(id=searchid)
    this_search.delete()
    this_search.save
    return# redirect('index')


def changesearchstate(request, searchid):
    this_search = Search.objects.get(id=searchid)
    this_search.state = True if this_search.state is False else False
    this_search.save()
    return# redirect('index')


def instructionpage(request):
    return render(request, 'externalhome.html', {})


def useroptions(request):
    return render(request, 'useroptions.html', {})


def deleteaccount(request, usernamematch):
    thisuser = request.user.username
    if usernamematch == thisuser:
        try:
            u = User.objects.get(username=thisuser)
            u.delete()
        except User.DoesNotExist:
            # username does not match
            return False
    else:
        # Some other error occurred if we get here
        # Left this in to not stop the process
        return False
    return True
