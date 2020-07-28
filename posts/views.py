from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


@cache_page(20, key_prefix="index_page")
def index(request):
    """
    Gets a selection of 10 entries per page.
    :param request:
    :return: page "index.html"
    """
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page, "paginator": paginator}
                  )


def group_posts(request, slug):
    """
    Gets an object from the database and outputs new entries by criteria.
    If the object is not found it reports a 404 error.

    :param request:
    :param slug:
    :return: page "group.html"
    """
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "group.html",
                  {"group": group,
                   "page": page,
                   "paginator": paginator, }
                  )


@login_required
def new_post(request):
    """
    Adds a new publication.
    :param request:
    :return: After validating the form and creating a new post,
    the author is redirected to the main page.
    """
    # Let"s assume that the http request body can"t be empty, then:
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, "posts/new_post.html", {"form": form, "is_edit": False})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect("index")


def profile(request, username):
    """
    Adds a profile page with posts
    :param request:
    :param username:
    :return: page "profile.html"
    """
    author = get_object_or_404(User, username=username)
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(user=request.user.id,
                                          author=author).exists()

    post_list = author.author_posts.all()
    count_posts = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "profile.html", {
        "author": author,
        "page": page,
        "paginator": paginator,
        "count_posts": count_posts,
        "profile": author,
        "following": following})


def post_view(request, username, post_id):
    """
    Creates a Page for viewing a separate post
    :param request:
    :param username:
    :param post_id:
    :return: page "post_view.html"
    """
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    count_posts = author.author_posts.count()

    form = CommentForm(request.POST)
    comments = post.comments.all()

    return render(request, "post_view.html", {
        "author": author,
        "username": username,
        "post": post,
        "count_posts": count_posts,
        "form": form,
        "comments": comments, })


@login_required
def post_edit(request, username, post_id):
    """
    Creating a page for editing an existing post
    :param request:
    :param username:
    :param post_id:
    :return: the page with the changed post or the page for viewing the post.
    """
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    if request.user != post.author:
        return redirect("post_view", username=username, post_id=post_id)

    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if not form.is_valid():
        return render(request, "posts/new_post.html", {
            "form": form,
            "post": post,
            "is_edit": True})
    form.save()
    return redirect("post_view", username=username, post_id=post_id)


@login_required
def add_comment(request, username, post_id):
    """
    Creating a comment for editing an existing post
    :param request:
    :param username:
    :param post_id:
    :return: the page with comment or the page for viewing the post.
    """
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    if not form.is_valid():
        return render(request, "includes/comments.html",
                      {"form": form, "post": post})
    comment = form.save(commit=False)
    comment.author = request.user
    comment.post = post
    form.save()
    return redirect("post_view", username, post_id)


@login_required
def follow_index(request):
    """
    Displays posts of authors that the current user is subscribed to.
    :param request:
    :return: the page with posts of authors that the current user is subscribed to.
    """
    author = get_object_or_404(User, username=request.user)
    post_list = Post.objects.filter(author__following__user=request.user)
    count_posts = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "follow.html",
                  {"author": author,
                   "count_posts": count_posts,
                   "page": page,
                   "paginator": paginator,
                   })


@login_required
def profile_follow(request, username):
    """
    Subscribes to an interesting author.
    """
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=request.user, author=author).exists()
    if not request.user == author and follow is False:
        Follow.objects.create(user=request.user, author=author)
    return redirect("profile", username=username)


@login_required
def profile_unfollow(request, username):
    """
    Unsubscribes from the author.
    """
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("profile", username=username)


def page_not_found(request,exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
