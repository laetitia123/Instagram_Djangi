from django.shortcuts import render,redirect

from django.http import HttpResponse, Http404,HttpResponseRedirect
import datetime as dt
from .models import *
# from .forms import NewsLetterForm
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from .forms import *
# Create your views here.
# Create your views here.
# @login_required(login_url='/accounts/login/') 
def profile(request):
    profile = Article.todays_news()
    return render(request, 'profile.html', {"profile":profile})
def news_today(request):
    date = dt.date.today()
    images= Image.todays_news()
    # return render(request, 'all-news/today-news.html', {"date": date,"news":news})
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            print('valid')
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = NewsLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)
            HttpResponseRedirect('news_today')
# After validating a form instance the values of the form are saved inside cleaned_data property which is a dictionary
    else:
        form = NewsLetterForm()
    return render(request, 'home.html', {"date": date,"images":images,"letterForm":form})

def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        # message =f"{ search_term }"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})
@login_required(login_url='/accounts/login/')       
def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})
@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect(news_today)

    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {"form": form})

@login_required(login_url='/accounts/login/')
def mine(request,username=None):
    if not username:
      username=request.user.username
      images = Image.objects.filter(name=username)
      user_object = request.user
  
    return render(request, 'myprofile.html', locals())
@login_required(login_url='/accounts/login/')
def edit(request):
    if request.method == 'POST':
        print(request.FILES)
        new_profile = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if new_profile.is_valid():
            new_profile.save()
            print(new_profile.fields)
        
            return redirect('myaccount')
    else:
        new_profile = ProfileForm(instance=request.user.profile)
    return render(request, 'edit.html', locals())