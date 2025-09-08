from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from .models import BlogPost, UserProfile, Bookmark, BlogImage, Vote, Comment
from django.contrib.auth.models import User
from .forms import BlogPostForm, UserProfileForm, CustomUserCreationForm, CommentForm
from .services.api import APIClient

def home(request):
    posts = BlogPost.objects.all().order_by('-created_at')[:6]
    return render(request, 'core/home.html', {'posts': posts})

def about(request):
    return render(request, 'core/about.html')

def team(request):
    # Using existing numbered images from static/img directory
    team_images = {
        'divyam_image': 'img/1.jpg',
        'abhinav_image': 'img/2.jpg',
        'hrick_image': 'img/3.jpg',
        'harsh_image': 'img/4.jpg'
    }
    return render(request, 'core/team.html', team_images)

def auth_view(request):
    login_form = AuthenticationForm()
    register_form = CustomUserCreationForm()
    
    if request.method == 'POST':
        action = request.POST.get('action', '')
        
        if action == 'login':
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Successfully logged in!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password.')
            
        elif action == 'register':
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                username = register_form.cleaned_data['username']
                
                if User.objects.filter(username=username).exists():
                    register_form.add_error('username', 'This username is already taken.')
                else:
                    try:
                        user = register_form.save()
                        login(request, user)
                        messages.success(request, 'Account created successfully! Welcome to Writoria.')
                        return redirect('home')
                    except Exception as e:
                        register_form.add_error(None, 'An error occurred during registration. Please try again.')
    
    return render(request, 'core/auth.html', {
        'login_form': login_form,
        'register_form': register_form
    })

class BlogListView(ListView):
    model = BlogPost
    template_name = 'core/blog_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['categories'] = BlogPost.CATEGORY_CHOICES
        return context

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'core/blog_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            context['is_bookmarked'] = Bookmark.objects.filter(
                user=self.request.user,
                post=self.object
            ).exists()
            context['user_vote'] = Vote.objects.filter(
                user=self.request.user,
                post=self.object
            ).first()
            
        context['comments'] = self.object.comments.filter(parent=None)
        context['comment_form'] = CommentForm()
        return context

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'core/blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        try:
            response = super().form_valid(form)
            
            # Handle additional images
            images = self.request.FILES.getlist('images')
            captions = form.cleaned_data.get('image_captions', '').split('\n')
            captions = [cap.strip() for cap in captions if cap.strip()]
            
            for i, image in enumerate(images):
                caption = captions[i] if i < len(captions) else ''
                BlogImage.objects.create(
                    post=self.object,
                    image=image,
                    caption=caption,
                    order=i
                )
            messages.success(self.request, 'Blog post created successfully!')
            return response
                
        except Exception as e:
            messages.error(self.request, f'Failed to create blog post: {str(e)}')
            return self.form_invalid(form)

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'core/blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        # Handle image updates
        images = self.request.FILES.getlist('images')
        captions = form.cleaned_data.get('image_captions', '').split('\n')
        captions = [cap.strip() for cap in captions if cap.strip()]
        
        # Delete existing images if replace_images is checked
        if form.cleaned_data.get('replace_images'):
            BlogImage.objects.filter(post=self.object).delete()
        
        # Add new images
        for i, image in enumerate(images):
            caption = captions[i] if i < len(captions) else ''
            BlogImage.objects.create(
                post=self.object,
                image=image,
                caption=caption,
                order=i + self.object.blogimage_set.count()
            )
        messages.success(self.request, 'Blog post updated successfully!')
        return response

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'core/blog_confirm_delete.html'
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect(success_url)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

@login_required
def toggle_bookmark(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        bookmark.delete()
        
    return JsonResponse({
        'is_bookmarked': created
    })

@login_required
def vote_post(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, slug=slug)
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={'is_life': True}
        )
        
        if not created:
            vote.is_life = not vote.is_life
            vote.save()
        
        # Update post votes count
        post.votes = Vote.objects.filter(post=post, is_life=True).count()
        post.save()
        
        return JsonResponse({
            'votes': post.votes,
            'has_life': vote.is_life
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def add_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = CommentForm({'content': data.get('content')})
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                parent_id = data.get('parent_id')
                if parent_id:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                
                comment.save()
                return JsonResponse({
                    'status': 'success',
                    'comment_id': comment.id,
                    'author': request.user.username,
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%b %d, %Y %H:%M'),
                    'parent_id': parent_id
                })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Parent comment not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    comment.delete()
    return JsonResponse({'status': 'success'})

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    user_posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    bookmarks = Bookmark.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'core/profile.html', {
        'form': form,
        'user_posts': user_posts,
        'bookmarks': bookmarks,
    })

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Calculate profile completion
    completion_fields = {
        'avatar': bool(profile.avatar),
        'bio': bool(profile.bio),
        'website': bool(profile.website)
    }
    profile_completion = (sum(completion_fields.values()) / len(completion_fields)) * 100
    
    return render(request, 'core/user_profile.html', {
        'profile': profile,
        'profile_completion': profile_completion
    })

def help_center(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject', 'No Subject')
            message = data.get('message')
            
            if name and email and message:
                # Submit to Flask API only
                api_response, status_code = APIClient.submit_contact_form(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message
                )
                
                if status_code == 201:
                    messages.success(request, 'Your message has been sent successfully! We\'ll get back to you soon.')
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Your message has been sent successfully! We\'ll get back to you soon.',
                        'redirect_url': '/'
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': api_response.get('message', 'An error occurred. Please try again.')
                    }, status=400)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please fill in all required fields.'
                }, status=400)
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            print(f"Error in help_center view: {str(e)}")  # Debug print
            return JsonResponse({
                'status': 'error',
                'message': 'An unexpected error occurred'
            }, status=500)
            
    return render(request, 'core/help_center.html')

def suggestion_form(request):
    if request.method == 'POST':
        try:
            response = requests.post(
                'http://localhost:5000/api/contact',
                json={
                    'name': request.POST.get('name'),
                    'email': request.POST.get('email'),
                    'subject': request.POST.get('subject', 'Site Suggestion'),
                    'message': request.POST.get('message')
                }
            )
            if response.status_code == 201:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Thank you for your suggestion!'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Something went wrong. Please try again.'
                }, status=400)
        except requests.RequestException:
            return JsonResponse({
                'status': 'error',
                'message': 'Could not connect to the server. Please try again later.'
            }, status=503)
    return render(request, 'core/suggestion_form.html')
