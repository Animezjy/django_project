from django.shortcuts import render


def post_list(request):
    return render(request, 'blog/post/list.html', locals())