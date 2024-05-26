from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.
from moviereview.forms import RegisterForm,LoginForm,ReviewForm
from moviereview.models import Movie,Review

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegisterForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        return render(request,"register.html",{"form":form})
    
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=request.POST.get("username")
            pwd=request.POST.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect('index')
            return render(request,"signin.html",{"form":form})
        return render(request,"signin.html",{"form":form})

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('signin')
    
class IndexView(View):
    def get(self,request,*args,**kwargs):
        qs=Movie.objects.all()
        trend=Movie.objects.filter(is_trending=True)
        return render(request,"index.html",{"movie":qs,"trending":trend})
    
class MovieDetailView(View):
    def get(self,request,*args,**kwargs):
        form=ReviewForm()
        id=kwargs.get("pk")
        qs=Movie.objects.get(id=id)
        return render(request,'moviedetail.html',{"movie":qs,"form":form})
    

class ReviewAddView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        movie_obj=Movie.objects.get(id=id)
        form=ReviewForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.movie=movie_obj
            form.save()
            return redirect('movie-detail',pk=id)
        return redirect('movie-detail',pk=id)
    

class UserReviewsView(View):
    def get(self,request,*args,**kwargs):
        qs=self.request.user.user_review.all().order_by('-created_date')
        return render(request,'userreviews.html',{"review":qs})


class MovieSearchView(View):
    def post(self,request,*args,**kwargs):
        movie=request.POST.get("box")
        qs=Movie.objects.filter(name__icontains=movie)
        return render(request,'search_results.html',{"movies":qs})
    
class ReviewLikeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Review.objects.get(id=id)
        qs.liked_by.add(request.user)
        qs.save()
        request.user.profile.liked_reviews.add(qs)
        return redirect('movie-detail',pk=qs.movie.id)
    
class ReviewUnLikeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Review.objects.get(id=id)
        qs.liked_by.remove(request.user)
        qs.save()
        request.user.profile.liked_reviews.remove(qs)
        return redirect('movie-detail',pk=qs.movie.id)