from django.shortcuts import render,redirect

from django.http import HttpResponse, Http404,HttpResponseRedirect
import datetime as dt
from .models import *
# from .forms import NewsLetterForm
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from .forms import *


@login_required(login_url='/accounts/login/') 
def news_today(request):
    date = dt.date.today()
    images= Image.todays_news()
    current_user=request.user
    myprof=Profile.objects.filter(id=current_user.id).first()
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
    return render(request, 'home.html', {"date": date,"images":images,"myprof":myprof,"letterForm":form})


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
    current_user=request.user
    pic_images=Image.objects.filter(user=current_user)
    # profile=Profile.objects.filter(user=current_user).first()
    if not username:
      username=request.user.username
      images = Image.objects.filter(name=username)
      user_object = request.user
  
    return render(request, 'myprofile.html', locals(),{"pic_images":pic_images})
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
    
@login_required(login_url='/accounts/login/')
def user(request, user_id):
    user_object = get_object_or_404(User, pk=user_id)
    if request.user == user_object:
        return redirect('myaccount')
    isfollowing = user_object.profile not in request.user.profile.follows
    user_images = user_object.profile.posts.all()
    user_liked = [like.photo for like in user_object.profile.mylikes.all()]
    return render(request, 'profile.html', locals())

@login_required(login_url='/accounts/login/')
def find(request, name):
    results = Profile.find_profile(name)
    return render(request, 'searchresults.html', locals())

@login_required(login_url='/accounts/login/')
def add_comment(request, image_id):
    current_user=request.user
    image_item=Image.objects.filter(id=image_id).first()
    prof=Profile.objects.filter(user=current_user.id).first()

  
    if request.method == 'POST':
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user.profile
            comment.post_by=prof
            comment.photo = image_item
        
            comment.save()
            return redirect("newsToday")
    else:
        form=CommentForm()
    return render(request,'comment.html',{"form":form,"image_id":image_id})


def search_results(request):

    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_users = Profile.search(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"users": searched_users})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})
def like_it(request,id):
     likes=1
     image=Image.objects.get(id=id)
     image.likes=image.likes+1
     image.save()
     return redirect("newsToday")