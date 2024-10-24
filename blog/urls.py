from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from blog import views


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('summernote/', include('django_summernote.urls')),
    path('about/', views.about, name='about'),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)