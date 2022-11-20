from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, RequestContext
from .forms import NewSearchForm, UserRegisterForm
from .models import Search, Result
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from .crawl import collect  # TODO remove this when CRON task is added to crawl.p as below

# Create your views here.


def index(request):

    #tempcrawltrigger()

    if request.method == "POST":
        if 'changestate' in request.POST.keys():
            changesearchstate(request, request.POST['changestate'])
        elif 'deletesearch' in request.POST.keys():
            removesearch(request, request.POST['deletesearch'])
        else:
            form = NewSearchForm(request.POST or None)
            if not form.is_valid(): print(form.errors)
            if form.is_valid():
                the_form = form.save(commit=False)
                the_form.user_id = request.user.id
                the_form.save()

    if request.user.is_authenticated:
        context = {}
        context['userResultList'] = []
        user_searches = Search.objects.filter(user_id=request.user.id)
        count = 0
        for item in user_searches:
            res = {}
            res['keyword'] = item.keyword
            res['url'] = item.url
            res['hits'] = count
            res['dateCreated'] = item.dateCreated
            res['hitIds'] = []
            res['state'] = "Enabled" if item.state else "Disabled"
            res['id'] = item.id
            search_results = Result.objects.filter(sourceSearch=item.id)
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
    return redirect('index')


def changesearchstate(request, searchid):
    this_search = Search.objects.get(id=searchid)
    this_search.state = True if this_search.state is False else False
    this_search.save()
    return redirect('index')


def instructionpage(request):
    return render(request, 'externalhome.html', {})

def tempcrawltrigger():
    # TODO This block will move into a CRON task at bottom of crawl.py. It is in views for
    # now to fire when loading the page for testing purposes
    # TODO url, search_word, div_id, and user should come from search table of database
    # TODO past_hits should come from results table of database
    url = 'https://prodogsdirect.org.uk/category/dogs/'
    search_word = 'Bulldog'
    div_id = 'entry-summary'
    user = ''
    past_hits = []

    found_word = collect(url, search_word, div_id)
    if found_word:
        for f in found_word:
            if f not in past_hits:
                print(f)  # TODO this will change to "report hit to database"
