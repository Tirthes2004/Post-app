"""
URL configuration for posts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('edit/<int:tweet_id>/', views.tweet_edit, name='tweet_edit'),
    path('delete/<int:tweet_id>/', views.tweet_delete, name='tweet_delete'),  # ✅ match `tweet_id`
    path('profile/', views.user_profile, name='profile'),
    path('accounts/', include('accounts.urls')),
    path('like-toggle/<int:tweet_id>/', views.like_toggle, name='like_toggle'),
    path('comment-add/<int:tweet_id>/', views.add_comment,  name='add_comment'),
    path('comments/<int:tweet_id>/',    views.view_comments,name='view_comments'),
    path('comment-edit/<int:comment_id>/',  views.edit_comment,   name='edit_comment'),
    path('comment-delete/<int:comment_id>/',views.delete_comment, name='delete_comment'),
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
