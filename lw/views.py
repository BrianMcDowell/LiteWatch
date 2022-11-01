from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, RequestContext
from .forms import NewSearchForm
from .models import Search
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
# Create your views here.


def index(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST or None)
        if not form.is_valid(): print(form.errors)
        if form.is_valid():
            the_form = form.save(commit=False)
            the_form.user_id = request.user.id
            the_form.save()

    if request.user.is_authenticated:
        print("Onto getting home page")
        context = {}
        context['userResultList'] = []
        user_searches = Search.objects.filter(user_id=request.user.id)
        count = 0
        for item in user_searches:
            print(item.url)
            res = {}
            res['keyword'] = item.keyword
            res['url'] = item.url
            res['hits'] = count
            res['dateCreated'] = item.dateCreated
            res['hitIds'] = "xyz123"
            res['state'] = "Enabled" if item.state else "Disabled"
            context['userResultList'].append(res)
            count += 3

        context['testText'] = "new text."
        #context['userResultList'].append(res)
        return render(request, 'home.html', context)
    else:
        return render(request, 'externalhome.html', {})


def login(request):
    # https://learndjango.com/tutorials/django-login-and-logout-tutorial
    template = loader.get_template('registration/login.html')
    return HttpResponse(template.render())


def newsearch(request):
    form = NewSearchForm()
    return render(request, 'newsearch.html', {'form':form})


def instructionpage(request):
    return render(request, 'externalhome.html', {})