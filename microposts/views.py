from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from accounts.models import Relationship, User
from .forms import PostCreateForm
from django.contrib import messages
from django.urls import reverse_lazy


# Create your views here.
class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'microposts/create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('microposts:create')
    
    def form_valid(self, form):
        # formに問題なければ、owner id に自分のUser idを割り当てる     
        # request.userが一つのセットでAuthenticationMiddlewareでセットされている。
        form.instance.owner_id = self.request.user.id
        messages.success(self.request, '投稿が完了しました')
        return super(PostCreateView, self).form_valid(form)
        
    def form_invalid(self, form):
        messages.warning(self.request, '投稿が失敗しました')
        return redirect('microposts:create')

class PostListView(LoginRequiredMixin, ListView):   # 追加
    # テンプレートを指定
    template_name = 'microposts/postlist.html'
    # 利用するモデルを指定
    model = Post
    # ページネーションの表示件数
    paginate_by = 5

    # Postsテーブルの全データを取得するメソッド定義
    # テンプレートでは、object_listとしてreturnの値が渡される
    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):  # 追加
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['favorite_list'] = user.favorite_post.all()

        return context

#更新は実装してない

#class PostDetailView(DetailView): # 追加
    # テンプレートを指定
    #template_name = 'microposts/myposts.html'
    # 利用するモデルを指定
    #model = Post
    # ページネーションの表示件数
    #paginate_by = 5
    #context_object_name = 'detail'
    
    # Postsテーブルのowner_idが自分自身の全データを取得するメソッド定義
    #def get_queryset(self):  # 自分の投稿オブジェクトを返す。
    #    qs = Post.objects.filter(owner_id=self.request.user)
    #    return qs

class PostDeleteView(LoginRequiredMixin, DeleteView):# 追加
    model = Post
    template_name = 'microposts/delete.html'
    
    # deleteviewでは、SuccessMessageMixinが使われないので設定する必要あり
    success_url = reverse_lazy('microposts:myposts')
    success_message = "投稿は削除されました。"
    # 削除された際にメッセージが表示されるようにする。
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

class MyPostsView(LoginRequiredMixin, ListView): # 追加
    # テンプレートを指定
    template_name = 'microposts/myposts.html'
    # 利用するモデルを指定
    model = Post
    # ページネーションの表示件数
    paginate_by = 5
    
    # Postsテーブルのowner_idが自分自身の全データを取得するメソッド定義
    def get_queryset(self):  # 自分の投稿オブジェクトを返す。
        return Post.objects.filter(owner_id=self.request.user)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        qs = Post.objects.filter(owner_id=self.request.user)
        # qsのレコード数をmy_posts_countというコンテキストとして設定

        # Postsテーブルの自分の投稿数をmy_posts_countへ格納 
        # context['my_posts_count'] = Post.objects.filter(owner_id=self.request.user).count()
        
        context['my_posts_count'] = qs.count()
        # Postsテーブルの全データを取得しpost_listへ格納
        context['favorite_list'] = user.favorite_post.all()
        context['following_list'] = Relationship.objects.filter(follower_id=user.id)
        # 自分がfollowしているidのみをmy_follow_listとして取得
        context['my_follow_list'] = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id', flat=True)
        # 自分がフォローしている人をfollowingsとして取得
        followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
        context['following_count'] = User.objects.filter(id__in=followings).count()
        # 自分をフォローしている人をfollowersとして取得
        followers = (Relationship.objects.filter(following_id=user.id)).values_list('follower_id')
        # context['followers_data] = User.objects.filter(id__in=followers).count()
        context['follower_count'] = followers.count()
        return context

class FollowersView(LoginRequiredMixin, ListView): # 追加
    # テンプレートを指定
    template_name = 'microposts/followers.html'
    # 利用するモデルを指定
    model = Relationship

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Postsテーブルの自分の投稿数をmy_posts_countへ格納
        context['my_posts_count'] = Post.objects.filter(owner_id=self.request.user).count()
        # 自分がフォローしている人をfollowingsとして取得
        followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
        # 自分がフォローしている人のオブジェクトを取得
        context['following_list'] = User.objects.filter(id__in=followings)
        # 自分がフォローしている人の数を取得
        context['following_count'] = User.objects.filter(id__in=followings).count()
        # 自分をフォローしている人をfollowersとして取得
        followers = (Relationship.objects.filter(following_id=user.id)).values_list('follower_id')
        # 自分をフォローしている人の数を取得
        context['follower_list'] = User.objects.filter(id__in=followers)
        return context

class FollowingView(LoginRequiredMixin, ListView): # 追加
    # テンプレートを指定
    template_name = 'microposts/followings.html'
    # 利用するモデルを指定
    model = Relationship

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Postsテーブルの自分の投稿数をmy_posts_countへ格納
        context['my_posts_count'] = Post.objects.filter(owner_id=self.request.user).count()
        # 自分がフォローしている人をfollowingsとして取得
        followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
        # 自分がフォローしている人のオブジェクトを取得
        context['following_list'] = User.objects.filter(id__in=followings)
        # 自分をフォローしている人をfollowersとして取得
        followers = (Relationship.objects.filter(following_id=user.id)).values_list('follower_id')
        # 自分をフォローしている人の数を取得
        context['follower_count'] = User.objects.filter(id__in=followers).count()
        return context    


def add_favorite(request, pk): # 追加
    # postのpkをhtmlから取得
    post = get_object_or_404(Post, pk=pk)
    # ログインユーザーを取得
    user = request.user
    # ログインユーザーをfavoritePostのUser_idとして、post_idは
    # 上で取得したPostを記録
    user.favorite_post.add(post)
    return redirect('microposts:postlist')

def remove_favorite(request, pk): # 追加
    # postのpkをhtmlから取得
    post = get_object_or_404(Post, pk=pk)
    # ログインユーザーを取得
    user = request.user
    # ログインユーザーをfavoritePostのUser_idとして、post_idは
    # 上で取得したPostを記録
    user.favorite_post.remove(post)
    return redirect('microposts:postlist')



# Create your views here.
