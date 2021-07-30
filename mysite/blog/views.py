from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from blog.models import Post
from blog.myforms import EmailPostForm, CommentForm


def post_list(request):
    posts = Post.published.all()
    object_list = Post.published.all()  # 筛选所有已发布的文章
    paginator = Paginator(object_list, 3)  # 每页显示3篇文章
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数不是一个整数就返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出总页数就返回最后一页
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', locals())


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, publish__year=year,
                             publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # 通过表单直接创建新数据对象，但是不要保存到数据库中
            new_comment = comment_form.save(commit=False)
            # 设置外键为当前文章
            new_comment.post = post
            # 将评论数据对象写入数据库
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/post_detail.html', locals())


# 分享文章
def post_share(request, post_id):
    # 获取到要分享的文章
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'z8794233@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', locals())
