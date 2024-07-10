from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import  CreateView

from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.utils import timezone
from datetime import timedelta

from posts.forms import CommentForm
from posts.models import Post, Category


# Create your views here.

def post_list(request,):
    categories = Category.objects.all()
    now = timezone.now()
    one_week = now - timedelta(days=7)
    week_post = Post.published.filter(publish_time__gte=one_week)
    week_post = sorted(week_post, key=lambda post: post.hit_count.hits, reverse=True)[:2]

    one_month = now - timedelta(days=30)
    month_post = Post.published.filter(publish_time__gte=one_month)
    month_post = sorted(month_post, key=lambda post: post.hit_count.hits, reverse=True)[:2]


    likes_post = Post.published.all()
    likes_post = sorted(likes_post, key=lambda post: post.hit_count.hits, reverse=True)[:2]

    post_list = Post.published.all().order_by('-publish_time')[:3]
    context = {
        "post_list": post_list,
        "categories": categories,
        "week_post": week_post,
        "month_post": month_post,
        "likes_post": likes_post
    }
    return render(request, "post_list.html", context)





def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.Published)



    context = {

    }
    hit_count = get_hitcount_model().objects.get_for_object(post)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits



    comments = post.comments
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "post": post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
            }
    comment_form = CommentForm()
    return render(request, 'post_detail.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_create.html"
    fields = ('title', 'body', 'image', 'category',)
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)







