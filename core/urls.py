from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/new/', views.BlogCreateView.as_view(), name='blog_create'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<slug:slug>/edit/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<slug:slug>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/<slug:slug>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('blog/<slug:slug>/vote/', views.vote_post, name='vote_post'),
    path('blog/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('auth/', views.auth_view, name='auth'),
    path('help/', views.help_center, name='help_center'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('suggestion/', views.suggestion_form, name='suggestion_form'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)