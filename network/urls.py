
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('followed_posts', views.followed_posts, name='followed_posts'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('save_post/<int:post_id>/', views.save_post, name='save_post'),
    path('like/<int:post_id>/', views.like, name='like'),
    path('comment/<int:post_id>/', views.comment, name='comment'),

    # autentication
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
