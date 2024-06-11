from django.views import generic
from django.db.models import Q
from blog.models import Post


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
            return qs.filter(
                status=Post.STATUS_PUBLISH
            ).filter(
                Q(content__contains=query) | Q(title__contains=query)
            )
        return qs.filter(status=Post.STATUS_PUBLISH)
