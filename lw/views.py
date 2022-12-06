from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import NewSearchForm, UserRegisterForm
from .models import Search, Result
from django.contrib.auth.models import User
from .crawl import test_search
from .cron import trigger

# Create your views here.


def index(request):
    """
    The 'main' function. If request is POST, performs appropriate
    task and then circles back as GET
    """
    # trigger()  # way to debug cron functionality.
    # Comment out or remove if not working on cron.
    if request.method == "POST":
        print(request.POST)
        if 'changestate' in request.POST.keys():
            changesearchstate(request, request.POST['changestate'])
        elif 'deletesearch' in request.POST.keys():
            removesearch(request, request.POST['deletesearch'])
        elif 'deleteaccount' in request.POST.keys():
            check = deleteaccount(request, request.POST['usernamematch'])
            if not check:
                return render(request, 'useroptions.html', {'FailedDelete': True})
        elif '_test' in request.POST.keys():
            email = request.user.email
            test_search(
                email,
                request.POST['url'],
                request.POST['keyword'],
                request.POST['elemtype'],
                request.POST['elemattr']
            )
            initial = {
                'keyword': request.POST['keyword'],
                'url': request.POST['url'],
                'elemtype': request.POST['elemtype'],
                'elemattr': request.POST['elemattr'],
            }
            form = NewSearchForm(initial=initial)
            return render(request, 'newsearch.html', {'form': form})
        else:
            form = NewSearchForm(request.POST or None)
            if not form.is_valid():
                print(form.errors)
            if form.is_valid():
                the_form = form.save(commit=False)
                the_form.user_id = request.user.id
                the_form.save()
                trigger()
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
    return render(request, 'externalhome.html', {})


def login(request):
    """user login"""
    # https://learndjango.com/tutorials/django-login-and-logout-tutorial
    template = loader.get_template('registration/login.html')
    return HttpResponse(template.render())


def register(request):
    """
    Checks for existing email/username
    If both are unique, registers a new user
    """
    # https://www.krazyprogrammer.com/2021/01/django-user-registration-in-pycharm.html
    # https://www.geeksforgeeks.org/django-sign-up-and-login-with-confirmation-email-python/
    msg = "The following are already in use: "
    duplicates = False
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                msg += email + " "
                duplicates = True
            if User.objects.filter(username=username).exists():
                msg += username + " "
                duplicates = True
            if not duplicates:
                form.save()
                return redirect('login')
    form = UserRegisterForm()
    context = {'form': form}
    if duplicates:
        context['msg'] = msg
    return render(request, 'registration.html', context)


def newsearch(request):
    """
    Adds a new search into the database
    Using NewSearchForm
    """
    form = NewSearchForm()
    return render(request, 'newsearch.html', {'form': form})


def removesearch(request, searchid):
    """
    Deletes specific search.
    Causes cascading deletion of associated search results
    """
    this_search = Search.objects.get(id=searchid)
    this_search.delete()


def changesearchstate(request, searchid):
    """Modifies the enable/disable state of a given search"""
    this_search = Search.objects.get(id=searchid)
    this_search.state = bool(not this_search.state)
    this_search.save()


def instructionpage(request):
    """
    External homepage and instruction
    page of LiteWatch
    """
    return render(request, 'externalhome.html', {})


def useroptions(request):
    """
    Loads user options page where
    user can delete account
    """
    return render(request, 'useroptions.html', {})


def deleteaccount(request, usernamematch):
    """
    Function to delete user's account.
    Verifies text box input given
    """
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
