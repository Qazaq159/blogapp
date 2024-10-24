from django.views import generic, View
from django.db.models import Q, Count, Case, When, IntegerField
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from rest_framework.authtoken.models import Token
from .models import Post, Tag, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=Post.STATUS_PUBLISH)
    template_name = 'index.html'


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


class SearchListView(generic.ListView):
    model = Post
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('query', '')

        if query:
            # Фильтрация по статусу публикации
            qs = qs.filter(status=Post.STATUS_PUBLISH).annotate(
                # Аннотация для сортировки по приоритету совпадений
                match_title=Count(Case(
                    When(title__icontains=query, then=1),
                    output_field=IntegerField()
                )),
                match_tags=Count(Case(
                    When(tags__name__icontains=query, then=1),
                    output_field=IntegerField()
                )),
                match_content=Count(Case(
                    When(content__icontains=query, then=1),
                    output_field=IntegerField()
                ))
            )

            # Фильтрация с учетом всех условий
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(tags__name__icontains=query) |
                Q(content__icontains=query)
            ).distinct()

            # Сортировка: сначала по совпадениям заголовков, затем по тегам, затем по содержимому
            qs = qs.order_by('-match_title', '-match_tags', '-match_content')

        # Если запрос пустой или результатов нет, перенаправляем на страницу со всеми постами
        if not query or not qs.exists():
            return redirect('/')  # Замените '/' на ваше имя URL для списка постов

        return qs


class PostCreateOrUpdateView(LoginRequiredMixin, View):
    template_name = 'post_form.html'

    def get(self, request, slug=None):
        if slug:
            post = get_object_or_404(Post, slug=slug)
        else:
            post = None

        tags = Tag.objects.all()  # Получаем все теги
        return render(request, self.template_name, {'post': post, 'tags': tags})

    def post(self, request, slug=None):
        # Извлечение токена из куки
        token_key = request.COOKIES.get('auth_token')
        user = None

        if token_key:
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
            except Token.DoesNotExist:
                messages.error(request, "Invalid token.")
                return redirect('login')  # Перенаправление на страницу входа

        if slug:
            post = get_object_or_404(Post, slug=slug)
        else:
            if user is None:
                messages.error(request, "You must be logged in to create a post.")
                return redirect('login')  # Перенаправление на страницу входа
            post = Post(author=user)  # Указываем автора здесь

        # Обновление полей поста
        post.title = request.POST.get('title')
        post.slug = slugify(post.title)
        post.content = request.POST.get('content')
        post.status = int(request.POST.get('status'))
        post.save()

        # Обновление тегов
        selected_tags = request.POST.getlist('tags')
        post.tags.set(selected_tags)

        messages.success(request, f"Post {'updated' if slug else 'created'} successfully.")
        return redirect('/')  # Переход на страницу со списком постов


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        messages.error(request, "You do not have permission to delete this post.")
        return redirect('post_detail', slug=slug)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('home')  # Замените 'home' на имя вашего URL для списка постов

    return render(request, '/', {'post': post})


class PostDetailView(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.all()  # Получаем все комментарии к посту
        return render(request, 'post_detail.html', {'post': post, 'comments': comments})

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        # Проверка на наличие авторизованного пользователя
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to add or edit a comment.")
            return redirect('post_detail', slug=slug)

        # Получение данных из POST-запроса
        content = request.POST.get('content')
        comment_id = request.POST.get('comment_id')

        if content:
            if comment_id:
                # Обновление существующего комментария
                try:
                    comment = Comment.objects.get(id=comment_id, post=post, author=request.user)
                    comment.content = content
                    comment.save()
                    messages.success(request, "Your comment has been updated.")
                except Comment.DoesNotExist:
                    messages.error(request, "You do not have permission to edit this comment.")
            else:
                # Создание нового комментария
                Comment.objects.create(
                    content=content,
                    post=post,
                    author=request.user
                )
                messages.success(request, "Your comment has been added.")
        else:
            messages.error(request, "Comment content cannot be empty.")

        return redirect('post_detail', slug=slug)


def delete_comment(request, slug, comment_id):
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, id=comment_id, post=post)

    if request.user == comment.author:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this comment.")

    return redirect('post_detail', slug=slug)
