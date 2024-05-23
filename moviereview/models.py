from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class Genre(models.Model):
    name=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    name=models.CharField(max_length=500)
    genre=models.ManyToManyField(Genre,related_name="genres")
    cast=models.CharField(max_length=500)
    storyline=models.CharField(max_length=500)
    image=models.ImageField(upload_to="images",default="default.jpg")
    director=models.CharField(max_length=300)
    writer=models.CharField(max_length=500)
    language=models.CharField(max_length=200,default="malayalam")
    runtime=models.CharField(max_length=200,default="2 hr")
    certification=models.CharField(max_length=200,default="U/A")
    year=models.PositiveIntegerField(default=2024)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_trending=models.BooleanField(default=False)
    trailer=models.CharField(max_length=500,null=True)
    banner=models.ImageField(upload_to="banners",default="default.jpg")

    def __str__(self):
        return self.name
    
    @property
    def Movie_reviews(self):
        qs=self.review.all().order_by("-created_date")
        return qs
    
    @property
    def average_rating(self):
        movie_reviews=self.Movie_reviews
        review_count=len(movie_reviews)
        avg_rating=0
        if movie_reviews:
            total_rating=sum([review.rating for review in movie_reviews])
            avg_rating=total_rating/float(review_count)
        return round(avg_rating,1)
    
    
class Review(models.Model):
    
    text=models.CharField(max_length=1000)
    options=((1,1),(1.5,1.5),(2,2),(2.5,2.5),(3,3),(3.5,3.5),(4,4),(4.5,4.5),(5,5))
    rating=models.FloatField(choices=options,default=4)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="review")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_review")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    liked_by=models.ManyToManyField(User)
    title=models.CharField(max_length=200,null=True)

    def __str__(self) -> str:
        return self.text

class UserProfile(models.Model):
    profile_picture=models.ImageField(upload_to="profilepics",null=True,blank=True)
    bio=models.CharField(max_length=200,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    wishlist=models.ManyToManyField(Movie,null=True)
    liked_reviews=models.ManyToManyField(Review,null=True)


def user_created(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(user_created,sender=User)
