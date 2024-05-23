from django.urls import path

from moviereview import views

urlpatterns=[
    path("register/",views.SignUpView.as_view(),name='signup'),
    path("",views.SignInView.as_view(),name='signin'),
    path("signout/",views.SignOutView.as_view(),name='signout'),
    path("index/",views.IndexView.as_view(),name='index'),
    path("movie/<int:pk>/",views.MovieDetailView.as_view(),name='movie-detail'),
    path("movie/<int:pk>/review/add/",views.ReviewAddView.as_view(),name='review-add'),
    path("movie/user/reviews/",views.UserReviewsView.as_view(),name="user-review")

]