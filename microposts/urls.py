from django.urls import path
from .views import (
   PostCreateView, PostListView, 
   PostDeleteView, MyPostsView, 
   FollowersView, FollowingView, 
   #PostDetailView# 追加
)
from . import views  # 追加

app_name = 'microposts'
urlpatterns = [
   path('create/', PostCreateView.as_view(), name='create'),
   path('postlist/', PostListView.as_view(), name='postlist'), 
   path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
   #path('detail/<int:pk>', PostDetailView.as_view(), name='detail'),
   path('myposts/', MyPostsView.as_view(), name='myposts'), # 追加
   path('add_favorite/<int:pk>/', views.add_favorite, name='add_favorite'), # 追加
   path('rm_favorite/<int:pk>/', views.remove_favorite, name='rm_favorite'), # 追加
   path('follower/', FollowersView.as_view(), name='follower'), # 追加
   path('following/', FollowingView.as_view(), name='following'), # 追加
]