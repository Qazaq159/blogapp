from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from blog import views
from blog.views import PostList, SearchListView, PostDetail, PostCreateOrUpdateView, post_delete, PostDetailView, delete_comment

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('search/', SearchListView.as_view(), name='search'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),  # Используем только PostDetailView
    path('post/create/', PostCreateOrUpdateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', PostCreateOrUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', post_delete, name='post_delete'),
    path('post/<slug:slug>/comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
